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
        project_lists = self.projectlist_set.all()
        for li in project_lists:
            self.number_task += li.projecttask_set.all().count()

        return self.number_task

    def save(self, *args, **kwargs):
        self.number_task = self.get_number_task
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['created_at']


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