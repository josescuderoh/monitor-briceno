# -*- coding: utf-8 -*-

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import UserProfile
from django import forms


# Login form
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Usuario", max_length=255,
                               widget=forms.TextInput(attrs={'class': 'loginput'}))
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput, required=True)


# Form used for users' registration
class UserProfileForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(render_value=True, attrs={'readonly': 'readonly'}),

                                label="Contraseña", help_text="Se asigna automáticamente")
    password2 = forms.CharField(widget=forms.PasswordInput(render_value=True, attrs={'readonly': 'readonly'}),
                                label="Confirmación de contraseña")

    """Form for registration of a new user"""
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name',
                  'position', 'phone', 'organization', 'address')


class UserProfileFormUpdate(forms.ModelForm):
    """Form used when an existing user is to be edited"""
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'first_name', 'last_name', 'position',
                  'phone', 'organization', 'organization_logo', 'address')

    def __init__(self, *args, **kwargs):
        super(UserProfileFormUpdate, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['organization'].widget.attrs['readonly'] = True
