# -*- coding: utf-8 -*-

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.signals import user_logged_in
from django.db import models


# User model manager
class UserProfileManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('El usuario debe tener una cuenta de correo asociada.')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          first_name=first_name,
                          last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""

        user = self.create_user(email, first_name, last_name, password, **extra_fields)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


# Modified user model for profiles
class UserProfile(AbstractUser, PermissionsMixin):
    """User model."""

    email = models.EmailField(max_length=255, unique=True, help_text="Preferiblemente correo institucional.")
    username = None
    first_name = models.CharField(max_length=255, verbose_name="Nombres")
    last_name = models.CharField(max_length=255, verbose_name="Apellidos")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    position = models.CharField(max_length=50, verbose_name="Cargo en la organización")
    phone = models.CharField(max_length=10, verbose_name="Teléfono")
    organization = models.CharField(max_length=50, verbose_name="Nombre de la organización")
    address = models.CharField(max_length=100, blank=True, null=True, verbose_name="Dirección (en territorio)")
    added = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(blank=True, null=True)
    login_count = models.IntegerField(default=0)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def get_short_name(self):
        """Returns the user's full name"""
        return self.first_name

    def get_full_name(self):
        """Returns the user's full name"""
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return 'Correo: ' + self.email + '; organización: ' + self.organization


def login_user(sender, request, user, **kwargs):
    user.login_count = user.login_count + 1
    user.save()
user_logged_in.connect(login_user)
