# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.utils import timezone
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import redirect
from django.db.models import Sum
from entities.models import UserProfile
from collections import defaultdict, Counter
from django.core.exceptions import PermissionDenied
from datetime import date
from rolepermissions.decorators import has_permission
from rolepermissions.mixins import HasPermissionsMixin
from rolepermissions.decorators import has_permission_decorator
from .models import Project, ProjectTask, Veredas
from .forms import CreateProjectForm, UpdateProjectForm, TaskFormSet, TaskFormSetUpdate, ImageFormSetUpdate
import xlwt
from .geojson_serializer import Serializer, ProjectSerializer
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
        if has_permission(self.request.user, 'view_projects'):
            if has_permission(self.request.user, 'view_all_projects'):
                projects_pk = [project.pk for project in Project.objects.filter().order_by('added')]
                for project_pk in projects_pk:
                    temp_tasks = [task.completion for task in ProjectTask.objects.filter(project=project_pk).order_by()]
                    if set(temp_tasks) == set(['Terminada']) and not Project.objects.get(id=project_pk).closed:
                        updated = Project.objects.get(id=project_pk)
                        updated.closed = True
                        updated.save()
                    elif set(temp_tasks) != set(['Terminada']) and Project.objects.get(id=project_pk).closed:
                        updated = Project.objects.get(id=project_pk)
                        updated.closed = False
                        updated.save()
                return Project.objects.all().order_by('start_date')
            else:
                projects_pk = [project.pk for project in Project.objects.filter(created_by=self.request.user).order_by('added')]
                for project_pk in projects_pk:
                    temp_tasks = [task.completion for task in ProjectTask.objects.filter(project=project_pk)]
                    if set(temp_tasks) == set(['Terminada']) and not Project.objects.get(id=project_pk).closed:
                        updated = Project.objects.get(id=project_pk)
                        updated.closed = True
                        updated.save()
                    elif set(temp_tasks) != set(['Terminada']) and Project.objects.get(id=project_pk).closed:
                        updated = Project.objects.get(id=project_pk)
                        updated.closed = False
                return Project.objects.filter(created_by=self.request.user).order_by('start_date')


class DetailView(generic.DetailView):
    """Detail view of projects."""
    model = Project
    template_name = 'projects/detail.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not (has_permission(request.user, 'view_all_projects') or (self.object.created_by == request.user)):
            raise PermissionError
        return super(DetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        # Assign values
        context = super(DetailView, self).get_context_data(**kwargs)
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


class ProjectCreate(HasPermissionsMixin, generic.CreateView):
    """View used to create a new projects"""
    # Assign data
    model = Project
    form_class = CreateProjectForm
    success_url = reverse_lazy('projects:projects-list')
    required_permission = 'create_projects'

    def get_context_data(self, **kwargs):
        # Assign values
        context = super(ProjectCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['task_formset'] = TaskFormSet(self.request.POST,
                                                  instance=self.object,
                                                  prefix='tasks')
            context['user'] = self.request.user
        else:
            context['task_formset'] = TaskFormSet(prefix='tasks')
        return context

    def form_valid(self, form):
        # Get context data
        context = self.get_context_data()
        # Assign current user to project
        form.instance.created_by = context['user']
        # Get formset
        formset = context['task_formset']
        # img_formset = context['image_formset']
        if formset.is_valid() and form.is_valid():
            self.object = form.save()
            formset.instance = self.object
            # img_formset.instance = self.object
            formset.save()
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class ProjectUpdate(generic.UpdateView):
    """View used to update the project fields and tasks"""
    model = Project
    template_name = 'projects/project_update_form.html'
    form_class = UpdateProjectForm
    success_url = reverse_lazy('projects:projects-list')

    def get_context_data(self, **kwargs):
        user = UserProfile.objects.get(pk=self.object.created_by.pk)
        if (self.request.user.id == user.id) or has_permission(self.request.user, 'edit_all_projects'):
            self.object = self.get_object()
            context = super(ProjectUpdate, self).get_context_data(**kwargs)
            if self.request.POST:
                context['task_formset'] = TaskFormSet(self.request.POST, instance=self.object)
            else:
                context['task_formset'] = TaskFormSetUpdate(instance=self.object)
            return context
        else:
            raise PermissionDenied

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


class ProjectAddImage(generic.UpdateView):
    """View used to add new images to the the project"""
    model = Project
    form_class = UpdateProjectForm
    template_name = 'projects/add_images.html'

    def get_context_data(self, **kwargs):
        user = UserProfile.objects.get(pk=self.object.created_by.pk)
        if (self.request.user.id == user.id) or has_permission(self.request.user, 'edit_all_projects'):
            self.object = self.get_object()
            context = super(ProjectAddImage, self).get_context_data(**kwargs)
            if self.request.POST:
                context['image_formset'] = ImageFormSetUpdate(self.request.POST,
                                                              self.request.FILES,
                                                              instance=self.object)
            else:
                context['image_formset'] = ImageFormSetUpdate()
            return context
        else:
            raise PermissionDenied

    def form_valid(self, form):
        context = self.get_context_data()
        img_formset = context['image_formset']
        if img_formset.is_valid() and form.is_valid():
            self.object = form.save()
            img_formset.instance = self.object
            img_formset.save()
            return HttpResponseRedirect(reverse('projects:project-update', kwargs={'pk': self.object.pk}))
        else:
            return self.render_to_response(self.get_context_data(form=form))


def ProjectMap(request, pk):
    """This method calls the geojson serializer created to build the data structure for the project's map"""
    geojson_serializer = ProjectSerializer()
    geojson_serializer.serialize(Veredas.objects.filter(project__pk=pk))
    data = geojson_serializer.getvalue()
    return HttpResponse(data, content_type='json')


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
        lineas_dict = {u"Briceño sostenible y protector del medio ambiente": 0,
                       u"Cambio para el desarrollo económico de Briceño": 0,
                       u"Briceño legal, transparente, seguro y en paz": 0,
                       u"Briceño con inclusión social para la paz": 0,
                       u"Ninguna": 0}

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
            'lineas_pd': {'categories': categories, 'dataset': dataset},
            'total_budget': Project.objects.aggregate(Sum('budget'))['budget__sum']
        }

        return Response(data)


class ReportView(generic.TemplateView):
    """Template view for report view"""
    template_name = "projects/report.html"


@has_permission_decorator('view_all_projects')
def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="proyectos.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Proyectos')

    # Sheet header, first row
    row_num = 0

    columns = [
        u"Entidad",
        u"Proyecto",
        u"Objetivo",
        u"Presupuesto",
        u"Interlocutor",
        u"Cerrado",
    ]

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 0

    rows = Project.objects.all().values_list('created_by__organization', 'name', 'main_goal', 'budget',
                                             'representative', 'closed')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response
