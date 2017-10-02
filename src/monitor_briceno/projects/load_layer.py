import os
from django.contrib.gis.utils import LayerMapping
from .models import Veredas

veredas_mapping = {
    'objectid' : 'OBJECTID',
    'dptompio' : 'DPTOMPIO',
    'codigo_ver' : 'CODIGO_VER',
    'nom_dep' : 'NOM_DEP',
    'nomb_mpio' : 'NOMB_MPIO',
    'nombre_ver' : 'NOMBRE_VER',
    'vigencia' : 'VIGENCIA',
    'fuente' : 'FUENTE',
    'descripcio' : 'DESCRIPCIO',
    'seudonimos' : 'SEUDONIMOS',
    'area_ha' : 'AREA_HA',
    'cod_dpto' : 'COD_DPTO',
    'shape_leng' : 'Shape_Leng',
    'shape_area' : 'Shape_Area',
    'geom' : 'MULTIPOLYGON',
}


veredas_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../static/data/veredas/ver_briceno.shp'))


def run(verbose=True):
    lm = LayerMapping(Veredas, veredas_shp, veredas_mapping, transform=False)
    lm.save(strict=True, verbose=verbose)
