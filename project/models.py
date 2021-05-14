from django.db import models
from user.models import User


class Project(models.Model):

    name = models.CharField(max_length=120)
    user_ids = models.ManyToManyField(User)
    is_creator_user = models.BooleanField(default=False)
