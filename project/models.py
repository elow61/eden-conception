from django.db import models
from user.models import User


class Project(models.Model):

    name = models.CharField(max_length=120, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='main_user')
    user_ids = models.ManyToManyField(User, related_name='member')

    def __str__(self):
        return self.name


class ProjectList(models.Model):

    name = models.CharField(max_length=100, unique=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ProjectTask(models.Model):

    name = models.CharField(max_length=120, unique=True)
    description = models.TextField()
    project_list = models.ForeignKey(ProjectList, on_delete=models.CASCADE)

    # Assign
    # Deadline : format date
    # Estimated time : format hour
    # Timesheet : OneToMany