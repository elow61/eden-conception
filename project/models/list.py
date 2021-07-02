from django.db import models
from django.db.models import F
from django.utils.timezone import now
from project.models.project import Project


class List(models.Model):

    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
