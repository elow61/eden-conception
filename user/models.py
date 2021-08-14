""" Inherit AbstractUser to add attributes """
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    ''' Inherit AbstractUser and add new fields '''
    email = models.EmailField(
        _('email address'),
        blank=True,
        unique=True,
        max_length=100
    )
    image = models.ImageField(default='default.png', upload_to='media')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
