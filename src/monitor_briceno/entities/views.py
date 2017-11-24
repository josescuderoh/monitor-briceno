# -*- coding: utf-8 -*-

from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.contrib.auth import login
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from rolepermissions.roles import assign_role
from rolepermissions.decorators import has_permission_decorator
from .forms import UserProfileForm, UserProfileFormUpdate
from .models import UserProfile
from .tasks import send_verification_email
from .tokens import account_activation_token
from rolepermissions.mixins import HasPermissionsMixin


@has_permission_decorator('create_users')
def register(request):
    """This view is used to render the registration form and create the new user in the database."""

    registered = False
    # If method is post
    if request.method == "POST":
        user_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid():
            # Store extra information
            user = user_form.save(commit=False)
            # Clean password
            password1 = user_form.cleaned_data['password1']
            user.set_password(password1)
            # Inactive until email confirmation
            user.is_active = False
            user.save()
            registered = True
            assign_role(user, user.role)
            # Send verification email
            site_domain = get_current_site(request).domain
            send_verification_email.delay(user.pk, site_domain)

        else:
            print(user_form.errors)
    # If method is get
    else:
        data = {'password1': "654321+*", 'password2': "654321+*"}
        user_form = UserProfileForm(initial=data)

    return render(request, 'entities/registration_form.html',
                  {'user_form': user_form,
                   'registered': registered})


def activate(request, uidb64, token):
    """This view is in charge of activation of the user once the email confirmation has
    been carried out."""
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserProfile.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, UserProfile.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponseRedirect('/projects/')
    else:
        return HttpResponse('El link de activación es inválido.')


@login_required
def edit_user(request, pk):
    """View used to edit the user information (only some variables are editable)"""

    updated = False

    user = UserProfile.objects.get(pk=pk)
    user_form = UserProfileFormUpdate(instance=user)

    if request.user.is_authenticated() and request.user.id == user.id:
        if request.method == "POST":
            user_form = UserProfileFormUpdate(request.POST, request.FILES, instance=user)

            if user_form.is_valid():
                created_user = user_form.save()
                created_user.save()
                updated = True

        return render(request, "entities/profile_form.html", {
            "noodle": pk,
            "user_form": user_form,
            "updated": updated,
        })
    else:
        raise PermissionDenied


class UsersView(HasPermissionsMixin, generic.ListView):
    """List view of all users and users management console"""
    template_name = 'entities/users.html'
    context_object_name = 'all_users'
    required_permission = 'create_users'

    def get_queryset(self):
        return UserProfile.objects.all().filter(groups__name='entidad').order_by('organization')
