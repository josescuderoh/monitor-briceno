from django.conf.urls import url
from . import views

app_name = 'projects'

urlpatterns = [
    # Maps url
    url(r'^mapas/$', views.MapView.as_view(), name='maps'),
    # Report url json
    url(r'^reporte/data/$', views.ReportData.as_view(), name='report-data'),
    # Report url
    url(r'^reporte/$', views.ReportView.as_view(), name='report'),
    # Url for json data of veredas
    url(r'^veredas_data/$', views.MapDataView, name='veredas'),
    # Projects url
    url(r'^$', views.ProjectsView.as_view(), name='projects-list'),
    # Download projects
    url(r'^export/xls/$', views.export_users_xls, name='export_users_xls'),
    # # Detail of projects url
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # API view for Detail
    url(r'^(?P<pk>[0-9]+)/map_data/$', views.ProjectMap, name='map-detail'),
    # Add project url
    url(r'^add/$', views.ProjectCreate.as_view(), name='project-add'),
    # Update project url
    url(r'^(?P<pk>[0-9]+)/edit/$', views.ProjectUpdate.as_view(),
        name='project-update'),
    # Add images using formset url
    url(r'^(?P<pk>[0-9]+)/add-images/$', views.ProjectAddImage.as_view(),
        name='project-images'),
]
