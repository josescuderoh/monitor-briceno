from django.contrib import admin
from .models import Veredas
from leaflet.admin import LeafletGeoAdmin


class VeredasAdmin(LeafletGeoAdmin):
    """Admin for Veredas data"""
    list_display = ('codigo_ver', 'nombre_ver')

admin.site.register(Veredas, VeredasAdmin)
