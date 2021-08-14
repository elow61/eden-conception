''' The model Project and his manager '''
from datetime import datetime
import calendar
from django.db import models
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from user.models import User


class ProjectManager(models.Manager):
    ''' The manager for the model project. '''

    def add_member(self, email, project):
        ''' Method to add a member into a project by the member's email. '''
        user = User.objects.filter(email__contains=email)

        if not user.exists() or user[0] in project.user_ids.all():
            return None

        project.user_ids.add(user.get().id)
        return user

    def get_number_task_by_list(self, project):
        ''' For the statistics of projects, this method is called
            to display the number task by lists into a project.
        '''
        datas = []
        for p_list in project.list_set.all():
            stats = {
                'list': p_list.name,
                'nb_task': p_list.task_set.all().count()
            }
            datas.append(stats)
        return datas

    def get_total_planned_hours(self, project):
        ''' For the statistics of projects, this method is called
            to display the total planned hours into a project.
        '''
        datas = []
        for p_list in project.list_set.all():
            tasks = p_list.task_set.all()
            total_planned_hours = sum(task.planned_hours for task in tasks)
            total_effective_hours = 0
            for task in tasks:
                to_convert = datetime.strptime(task.effective_hours_time, '%H:%M').time()
                total_effective_hours += to_convert.hour + to_convert.minute / 60.0

            stats = {
                'list': p_list.name,
                'planned_hours': total_planned_hours,
                'effective_hours': total_effective_hours
            }
            datas.append(stats)
        return datas

    def get_history_time_work(self, project, List, Task, Timesheet):
        ''' Get the total time work (effective hours) for a project.
            return a dict with the keys is month and values is the total time work
            like this : {'June': 8, 'July': 9}
        '''
        project_list = List.objects.filter(project=project)
        project_task = Task.objects.filter(project_list__in=project_list)

        datas = list(Timesheet.objects.filter(
            task__in=project_task
        ).order_by().annotate(
            month=ExtractMonth('created_at')).values('month').annotate(data_sum=Sum('unit_hour')))
        for val in datas:
            val['month'] = calendar.month_name[val['month']]

        return datas

    def get_projects(self, user):
        ''' Get the list of projects with the projects of members. '''
        queryset = Project.objects.none()
        queryset |= user.main_user.all()
        queryset |= user.member.all()
        return queryset.distinct()

    def get_members(self, user):
        ''' Get the members added into the projects of main user '''
        projects = Project.objects.filter(user_id=user.id)
        members = User.objects.none()

        for project in projects:
            if project.user_id == user.id:
                members |= project.user_ids.all().exclude(id=user.id)

        return members.distinct()


class Project(models.Model):
    ''' Class to have one or many project '''
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
        ''' Method to calculate the field number_task
            and get the number of task into the project.
        '''
        self.number_task = 0
        project_lists = self.list_set.all()
        for p_list in project_lists:
            self.number_task += p_list.task_set.all().count()

        return self.number_task

    def save(self, *args, **kwargs):
        self.number_task = self.get_number_task
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)

    class Meta:
        ''' used to ordering the model '''
        ordering = ['created_at']
