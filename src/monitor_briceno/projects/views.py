# -*- coding: utf-8 -*-

from django.http import Http404, HttpResponse
from django.views import generic
from django.utils import timezone
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from entities.models import UserProfile
from collections import defaultdict, Counter
from datetime import date
from .models import Project, ProjectTask, Veredas
from .forms import CreateProjectForm, UpdateProjectForm, TaskFormSet, TaskFormSetUpdate

from .geojson_serializer import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response


# Default views
class HomeView(generic.TemplateView):
    template_name = 'projects/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        return context


class LastAccessMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            current_profile = UserProfile.objects.get(pk=request.user.pk)
            current_profile.last_activity = timezone.now()
            current_profile.save()
        return super(LastAccessMixin, self).dispatch(request, *args, **kwargs)


class ProjectsView(LastAccessMixin, generic.ListView):
    """List view of all projects given specific permissions"""
    template_name = 'projects/projects.html'
    context_object_name = 'all_projects'

    def get_queryset(self):
        # Check if user is authenticated
        if not self.request.user.is_authenticated:
            raise Http404
        else:
            if self.request.user.is_superuser:
                projects_pk = [project.pk for project in Project.objects.filter().order_by('added')]
                for project_pk in projects_pk:
                    temp_tasks = [task.completion for task in ProjectTask.objects.filter(project=project_pk).order_by()]
                    if set(temp_tasks) == set(['Terminada']) and not Project.objects.get(id=project_pk).closed:
                        updated = Project.objects.get(id=project_pk)
                        updated.closed = True
                        updated.save()
                return Project.objects.all()
            else:
                projects_pk = [project.pk for project in Project.objects.filter(created_by=self.request.user).order_by('added')]
                for project_pk in projects_pk:
                    temp_tasks = [task.completion for task in ProjectTask.objects.filter(project=project_pk)]
                    if set(temp_tasks) == set(['TE']) and not Project.objects.get(id=project_pk).closed:
                        updated = Project.objects.get(id=project_pk)
                        updated.closed = True
                        updated.save()
                return Project.objects.filter(created_by=self.request.user)


class DetailView(generic.DetailView):
    """Detail view of projects."""
    model = Project
    template_name = 'projects/detail.html'

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        # Assign values
        context = super().get_context_data(**kwargs)
        # Calculate days
        start = self.object.start_date
        end = self.object.end_date
        today = date.today()
        # Get difference
        final_delta = end - start
        current_delta = today - start
        # Check delta time
        if final_delta >= current_delta:
            context['final_delta'] = final_delta
            context['current_delta'] = current_delta
        else:
            context['final_delta'] = final_delta
            context['current_delta'] = final_delta
        return context


class ProjectCreate(generic.CreateView):
    """View used to create a new projects"""
    # Assign data
    model = Project
    form_class = CreateProjectForm
    success_url = reverse_lazy('projects:projects-list')

    def get_context_data(self, **kwargs):
        # Check if user is authenticated
        if not self.request.user.is_authenticated:
            raise Http404
        else:
            # Assign values
            context = super(ProjectCreate, self).get_context_data(**kwargs)
            if self.request.POST:
                context['task_formset'] = TaskFormSet(self.request.POST)
                context['user'] = self.request.user
            else:
                context['task_formset'] = TaskFormSet()
            return context

    def form_valid(self, form):
        # Get context data
        context = self.get_context_data()
        # Assign current user to project
        form.instance.created_by = context['user']
        # Get formset
        formset = context['task_formset']
        if formset.is_valid() and form.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class ProjectUpdate(generic.UpdateView):
    """View used to update the project fields and tasks"""
    model = Project
    form_class = UpdateProjectForm
    success_url = reverse_lazy('projects:projects-list')

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super(ProjectUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['task_formset'] = TaskFormSetUpdate(self.request.POST, instance=self.object)
        else:
            context['task_formset'] = TaskFormSetUpdate(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['task_formset']
        if formset.is_valid() and form.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))


def MapDataView(request):
    """This method calls the geojson serializer created to build the data structure for the maps"""
    geojson_serializer = Serializer()
    geojson_serializer.serialize(Veredas.objects.all())
    data = geojson_serializer.getvalue()
    return HttpResponse(data, content_type='json')


class MapView(generic.TemplateView):
    """Template view for maps view"""
    template_name = 'projects/map.html'


class ReportData(APIView):
    """This view generates the data required to display the report url"""
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        projects_per_organization = dict(Counter([project.created_by.organization for project in Project.objects.all()]))
        projects_data = [(project.created_by.organization, project.budget) for project in Project.objects.all()]
        projects_per_vereda = dict(Counter([ver.nombre_ver for project in Project.objects.all() for ver in project.coverage.all()]))
        representatives = dict(Counter([project.representative for project in Project.objects.all()]))
        beneficiary = dict(Counter([project.beneficiary for project in Project.objects.all()]))
        status = dict(Counter([project.status for project in Project.objects.all()]))
        lineas_pd = dict(Counter([project.lines_pd for project in Project.objects.all()]))

        # Process data
        d = defaultdict(int)
        for (org, monto) in projects_data:
            d[(org)] += monto
        budget_per_organization = {k: v for k, v in d.items()}

        # Process status data
        key_map = {0: 'Por iniciar', 1: 'En curso', 2: 'Finalizado'}
        statuses = {key_map[key]: val for key, val in status.items()}

        # Process lineas_pd data
        lineas_dict = {"Briceño sostenible y protector del medio ambiente": 0,
                       "Cambio para el desarrollo económico de Briceño": 0,
                       "Briceño legal, transparente, seguro y en paz": 0,
                       "Briceño con inclusión social para la paz": 0,
                       "Ninguna": 0}

        # Create objects required for radar data
        category = []
        lineas_data = []

        for k, v in lineas_dict.items():
            if k in lineas_pd.keys():
                category.append({'label': k})
                lineas_data.append({'value': lineas_pd[k]})
            else:
                category.append({'label': k})
                lineas_data.append({'value': 0})
        categories = [
            {
                "category": category
            }
        ]
        dataset = [
            {"seriesname": "Cantidad de proyectos",
             "data": lineas_data
             }
        ]

        data = {
            'names': [proj[0] for proj in projects_data],
            'no_projects': len(projects_data),
            'no_entities': len(projects_per_organization.keys()),
            'no_veredas': len(projects_per_vereda.keys()),
            'projects_per_organization': [{'label': k, 'value': v} for k, v in projects_per_organization.items()],
            'budget_per_organization': [{'label': k, 'value': v} for k, v in budget_per_organization.items()],
            'representative': [{'label': k, 'value': v} for k, v in representatives.items()],
            'beneficiary': [{'label': k, 'value': v} for k, v in beneficiary.items()],
            'statuses': [{'label': k, 'value': v} for k, v in statuses.items()],
            'lineas_pd': {'categories': categories, 'dataset': dataset}
        }

        return Response(data)


class ReportView(generic.TemplateView):
    """Template view for report view"""
    template_name = "projects/report.html"
