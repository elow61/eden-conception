from django.db import models
from project.models import Task
from user.models import User


class Timesheet(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    description = models.CharField(max_length=200)
    unit_hour = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True, default='00:00')
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
