from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import UserProfile
from django import forms


# Login form
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Correo", max_length=255,
                               widget=forms.TextInput(attrs={'class': 'loginput'}))
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput, required=True)


# Form used for users' registration
class UserProfileForm(UserCreationForm):
    """Form for registration of a new user"""
    class Meta:
        model = UserProfile
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name',
                  'position', 'phone', 'organization', 'address')


class UserProfileFormUpdate(forms.ModelForm):
    """Form used when an existing user is to be edited"""
    class Meta:
        model = UserProfile
        fields = ('email', 'first_name', 'last_name', 'position',
                  'phone', 'organization', 'address')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['organization'].widget.attrs['readonly'] = True
