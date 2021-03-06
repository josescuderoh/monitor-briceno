from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm

app_name = 'entities'

urlpatterns = [
    # # User registration url
    url(r'^register/$', views.register, name='register'),
    # Activate account
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    # Edit profile url
    url(r'^profile/(?P<pk>[0-9]+)/$', views.edit_user, name='profile-update'),
    # Login url
    url(r'^login/$', auth_views.login, {'template_name': 'entities/login.html',
                                        'authentication_form': LoginForm}, name='login'),
    # Logout url
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    # List of Users
    url(r'^users/$', views.UsersView.as_view(), name='users'),
    # Delete user
    url(r'^delete/(?P<pk>[0-9]+)/$', views.DeleteUser.as_view(), name='delete-user'),
]
