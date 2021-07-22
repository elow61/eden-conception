from django.db import models
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from user.models import User
from datetime import datetime
import calendar


class ProjectManager(models.Manager):

    def add_member(self, email, project):
        user = User.objects.filter(email__contains=email)

        if not user.exists():
            return

        project.user_ids.add(user.get().id)
        return user

    def get_number_task_by_list(self, project):
        datas = []
        for li in project.list_set.all():
            stats = {
                'list': li.name,
                'nb_task': li.task_set.all().count()
            }
            datas.append(stats)
        return datas

    def get_total_planned_hours(self, project):
        datas = []
        for li in project.list_set.all():
            tasks = li.task_set.all()
            total_planned_hours = sum(task.planned_hours for task in tasks)
            total_effective_hours = 0
            for task in tasks:
                to_convert = datetime.strptime(task.effective_hours_time, '%H:%M').time()
                total_effective_hours += to_convert.hour + to_convert.minute / 60.0

            stats = {
                'list': li.name,
                'planned_hours': total_planned_hours,
                'effective_hours': total_effective_hours
            }
            datas.append(stats)
        return datas

    def get_history_time_work(self, project, List, Task, Timesheet):
        project_list = List.objects.filter(project=project)
        project_task = Task.objects.filter(project_list__in=project_list)

        datas = list(Timesheet.objects.filter(
            task__in=project_task
        ).order_by().annotate(month=ExtractMonth('created_at')).values('month').annotate(data_sum=Sum('unit_hour')))
        for val in datas:
            val['month'] = calendar.month_name[val['month']]

        return datas


class Project(models.Model):

    name = models.CharField(max_length=120, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='main_user')
    user_ids = models.ManyToManyField(User, related_name='member')
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    number_task = models.IntegerField(default=0)

    objects = models.Manager()
    objects_project = ProjectManager()

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
