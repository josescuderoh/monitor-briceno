from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms


# Login forms
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Correo", max_length=255,
                               widget=forms.TextInput(attrs={'class': 'loginput'}))
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput, required=True)
