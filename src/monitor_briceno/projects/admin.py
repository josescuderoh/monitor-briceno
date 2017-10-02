from django.contrib import admin
from .models import Veredas, Project, ProjectTask
from leaflet.admin import LeafletGeoAdmin


class ProjectTaskInline(admin.StackedInline):
    model = ProjectTask
    extra = 0


class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectTaskInline, ]
    list_display = ('name', 'created_by')


class VeredasAdmin(LeafletGeoAdmin):
    """Admin for Veredas data"""
    list_display = ('codigo_ver', 'nombre_ver')

admin.site.register(Veredas, VeredasAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectTask)
