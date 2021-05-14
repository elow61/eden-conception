""" Inherit AbstractUser to add attributes """
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
# from project.models import Project


class User(AbstractUser):

    email = models.EmailField(
        _('email address'),
        blank=True,
        unique=True,
        max_length=100
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
