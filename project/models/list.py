''' The model List  '''
from django.db import models
from project.models.project import Project


class List(models.Model):
    ''' Class to create lists into a project '''
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)
