from django.db import models
from django.utils.timezone import now
from user.models import User


class Project(models.Model):

    name = models.CharField(max_length=120, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='main_user')
    user_ids = models.ManyToManyField(User, related_name='member')
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    number_task = models.IntegerField(default=0)

    @property
    def get_number_task(self):
        self.number_task = 0
        project_lists = self.list_set.all()
        for li in project_lists:
            self.number_task += li.task_set.all().count()

        return self.number_task

    def save(self, *args, **kwargs):
        self.number_task = self.get_number_task
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['created_at']


class List(models.Model):

    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Task(models.Model):

    name = models.CharField(max_length=120)
    description = models.TextField()
    project_list = models.ForeignKey(List, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    deadline = models.DateField(blank=True, null=True)
    index = models.IntegerField(db_index=True)
    planned_hours = models.TimeField(auto_now=False, auto_now_add=False, default='00:00')
    effective_hours = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    remaining_hours = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)

    class Meta:
        ordering = ['index']
