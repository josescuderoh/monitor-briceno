from django.conf.urls import url
from . import views

app_name = 'projects'

urlpatterns = [
    # Index view
    url(r'^$', views.HomeView.as_view(), name='home'),
    # Maps url
    url(r'^mapas/$', views.MapView.as_view(), name='maps'),
    # Report url json
    url(r'^reporte/data/$', views.ReportData.as_view(), name='report-data'),
    # Report url
    url(r'^reporte/$', views.ReportView.as_view(), name='report'),
    # Url for json data of veredas
    url(r'^veredas_data/$', views.MapDataView, name='veredas'),
    # Projects url
    url(r'^list/$', views.ProjectsView.as_view(), name='projects-list'),
    # # Detail of projects url
    url(r'^projects/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # Add project url
    url(r'^projects/add/$', views.ProjectCreate.as_view(), name='project-add'),
    # Update project url
    url(r'^projects/(?P<pk>[0-9]+)/edit/$', views.ProjectUpdate.as_view(), name='project-update'),
]
