# -*- coding: utf-8 -*-

from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from .models import Project, ProjectTask, ProjectImage
from django.forms.widgets import DateInput
from django import forms


class CreateProjectForm(ModelForm):
    """Form to create a new project"""
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CreateProjectForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['created_by', 'closed']
        widgets = {
            'start_date': DateInput(attrs={'type': 'date',
                                           'placeholder': 'dd/mm/aaaa'}),
            'end_date': DateInput(attrs={'type': 'date',
                                         'placeholder': 'dd/mm/aaaa'}),
            'main_goal': forms.Textarea(attrs={'rows': 3}),
            'beneficiary_comments': forms.Textarea(attrs={'rows': 4}),
        }


class CreateTaskForm(ModelForm):
    """Form to create a new task for a given project"""

    class Meta:
        model = ProjectTask
        fields = '__all__'

TaskFormSet = inlineformset_factory(Project, ProjectTask,
                                    extra=1, fields='__all__',
                                    max_num=3, can_delete=False,
                                    form=CreateTaskForm)


class UpdateProjectForm(ModelForm):
    """Form used when an existing project is to be edited"""

    name = forms.CharField(disabled=True, label='Nombre del Proyecto')
    main_goal = forms.CharField(disabled=True, label='Objetivo principal', widget=forms.Textarea(attrs={'rows': 3}))
    beneficiary = forms.CharField(disabled=True, label='Beneficiarios')
    no_benef = forms.IntegerField(disabled=True, label='Número de Beneficiarios')
    start_date = forms.DateField(disabled=True, label='Fecha de inicio')
    end_date = forms.DateField(disabled=True, label='Fecha de finalización')
    budget = forms.IntegerField(disabled=True, label='Monto de ejecución')
    representative = forms.CharField(disabled=True, label='Interlocutor')
    lines_pd = forms.CharField(disabled=True, label='Líneas del plan que impactan')

    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['created_by', 'coverage', 'closed']
        widgets = {
            'beneficiary_comments': forms.Textarea(attrs={'rows': 2}),
        }


class UpdateTaskForm(ModelForm):
    """Form used when tasks of an existing project are to be edited"""
    class Meta:
        model = ProjectTask
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UpdateTaskForm, self).__init__(*args, **kwargs)
        self.fields['task'].widget.attrs['readonly'] = True

TaskFormSetUpdate = inlineformset_factory(Project, ProjectTask,
                                          extra=0, fields='__all__',
                                          can_delete=False, max_num=3,
                                          form=UpdateTaskForm)


class UpdateImageForm(ModelForm):
    """Form used when images of an existing project are to be added"""
    class Meta:
        model = ProjectImage
        fields = '__all__'


ImageFormSetUpdate = inlineformset_factory(Project, ProjectImage,
                                           extra=1, fields='__all__',
                                           can_delete=False, max_num=10,
                                           form=UpdateImageForm)
