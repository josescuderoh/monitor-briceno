# -*- coding: utf-8 -*-

from django.db import models
from entities.models import UserProfile
from django.contrib.gis.db import models as geo_models
from django.core.urlresolvers import reverse
from datetime import date
from django.core.exceptions import ValidationError


class Veredas(models.Model):
    """Model for shapes and data from veredas"""
    objectid = models.IntegerField()
    dptompio = models.CharField(max_length=80)
    codigo_ver = models.CharField(max_length=80)
    nom_dep = models.CharField(max_length=80)
    nomb_mpio = models.CharField(max_length=80)
    nombre_ver = models.CharField(max_length=80)
    vigencia = models.CharField(max_length=80)
    fuente = models.CharField(max_length=80)
    descripcio = models.CharField(max_length=80)
    seudonimos = models.CharField(max_length=250)
    area_ha = models.FloatField()
    cod_dpto = models.CharField(max_length=80)
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    geom = geo_models.MultiPolygonField(srid=4326)

    def __str__(self):
        return self.nombre_ver

    class Meta:
        verbose_name = "Vereda"
        verbose_name_plural = "Veredas"


# Create project class
class Project(models.Model):
    """Model for projects of each entity"""
    # Usuario
    created_by = models.ForeignKey(UserProfile, related_name='created_by', on_delete=models.CASCADE)
    # Nombre del proyecto
    name = models.CharField(verbose_name="Nombre del proyecto", max_length=250)
    # Objetivo de impacto
    main_goal = models.CharField(verbose_name="Objetivo principal", max_length=500)
    # Destinatario de la ejecución
    BENEF_CHOICES = (("Individuos", "Individuos"),
                     ("Instituciones", "Instituciones"),
                     ("Familias", "Familias"))
    beneficiary = models.CharField(verbose_name="Tipo de beneficiarios", choices=BENEF_CHOICES, max_length=30)
    beneficiary_comments = models.CharField(verbose_name="Observaciones sobre los beneficiarios",
                                            max_length=100, blank=True, null=True)
    # Cantidad de beneficiarios
    no_benef = models.IntegerField(verbose_name="Número de beneficiarios")
    # Fecha de inicio
    start_date = models.DateField(verbose_name="Fecha de inicio", help_text="Seleccionar en el calendario.")
    # Fecha de finalización
    end_date = models.DateField(verbose_name="Fecha de finalización", help_text="Seleccionar en el calendario.")
    # #Cobertura en las veredas
    coverage = models.ManyToManyField(Veredas, verbose_name="Veredas beneficiadas",
                                      help_text="Usar Crtl para seleccionar más de una opción.")
    # Monto de ejecución
    budget = models.IntegerField(verbose_name="Monto de ejecución",
                                 help_text='Cifra en pesos colombianos',
                                 blank=True, null=True)
    # Dependencia de la alcaldía
    MUN_CHOICES = (
        ("Ninguna", "Ninguna"),
        ("Secretaría de Gobierno y Servicios Administrativos", "Secretaría de Gobierno y Servicios Administrativos"),
        ("Secretaría Local de Salud", "Secretaría Local de Salud"),
        ("Tesorería de Rentas", "Tesorería de Rentas"),
        ("Secretaría de Planeación y Obras Municipales", "Secretaría de Planeación y Obras Municipales"),
        ("Secretaría para la Educación para la Cultura y el Desarrollo", "Secretaría para la Educación para la Cultura y el Desarrollo"))
    representative = models.CharField(verbose_name="Interlocutor en el municipio", max_length=200, choices=MUN_CHOICES)
    # Linea del plan a la cual impactan
    PD_CHOICES = (
        ("Ninguna", "Ninguna"),
        ("Briceño con inclusión social para la paz", "Briceño con inclusión social para la paz"),
        ("Cambio para el desarrollo económico de Briceño", "Cambio para el desarrollo económico de Briceño"),
        ("Briceño legal, transparente, seguro y en paz", "Briceño legal, transparente, seguro y en paz"),
        ("Briceño sostenible y protector del medio ambiente", "Briceño sostenible y protector del medio ambiente")
    )
    lines_pd = models.CharField(verbose_name="Líneas del plan de desarrollo que impacta", max_length=200, choices=PD_CHOICES)
    # Se ha cerrado el proyecto
    closed = models.BooleanField(default=False)
    # Control de cambios
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # How to show it
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"

    def get_absolute_url(self):
        reverse('projects:detail', kwargs={'pk': self.pk})

    @property
    def status(self):
        if date.today() < self.start_date and not self.closed:
            return 0
        elif (date.today() <= self.end_date and date.today() >= self.start_date) and not self.closed:
            return 1
        else:
            return 2

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError('Fecha de finalización inválida')
        elif self.end_date < date.today():
            raise ValidationError('Fecha de finalización inválida')


# Associated tasks to project
class ProjectTask(models.Model):
    """Tasks or activities defined inside each project"""
    # ID del proyecto
    project = models.ForeignKey(Project, related_name="tasks")
    # Tarea
    task = models.CharField(verbose_name="Actividad", max_length=50)
    # Nivel de ejecución
    LEVELS = (('Por iniciar', 'Por iniciar'), ('En curso', 'En curso'), ('Terminada', 'Terminada'))
    completion = models.CharField(verbose_name="Estado de ejecución",
                                  choices=LEVELS, default=False, max_length=20)
    # Observaciones
    comments = models.CharField(verbose_name="Observaciones", max_length=100, blank=True, null=True)
    # Control de cambios
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tarea del proyecto"
        verbose_name_plural = "Tareas"
