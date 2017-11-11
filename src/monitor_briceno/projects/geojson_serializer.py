from django.core import serializers
from .models import Veredas

GeoJSONSerializer = serializers.get_serializer("geojson")


class Serializer(GeoJSONSerializer):
    """GeoJSONSerializer for including new properties in maps"""
    def get_dump_object(self, obj):
        data = super(Serializer, self).get_dump_object(obj)
        # Extend to your taste
        data.update(num_proj=Veredas.objects.get(pk=obj.pk).project_set.all().count())
        data.update(entities=list(set(Veredas.objects.filter(pk=obj.pk, project__created_by__organization__isnull=False).
                    values_list('project__created_by__organization', flat=True).all())))
        return data


class ProjectSerializer(GeoJSONSerializer):
    """GeoJSONSerializer for project's map"""

    def get_dump_object(self, obj, **kwargs):
        data = super(ProjectSerializer, self).get_dump_object(obj)
        data.update(included=True)
        return data
