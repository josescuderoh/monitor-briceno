from django.core import serializers
from .models import Veredas
from django.db.models import Sum

GeoJSONSerializer = serializers.get_serializer("geojson")


class Serializer(GeoJSONSerializer):
    """GeoJSONSerializer for including new properties in maps"""
    def get_dump_object(self, obj):
        data = super(Serializer, self).get_dump_object(obj)
        # Extend to your taste
        data.update(num_proj=Veredas.objects.get(pk=obj.pk).project_set.all().count())
        data.update(investment=Veredas.objects.filter(pk=obj.pk).annotate(investment=Sum('project__budget'))[0].investment)
        data.update(entities=list(set(Veredas.objects.filter(pk=obj.pk, project__created_by__organization__isnull=False).
                    values_list('project__created_by__organization', flat=True).all())))
        return data
