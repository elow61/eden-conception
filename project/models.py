from django.db import models
from django.db.models import F
from django.utils.timezone import now
from user.models import User


class ProjectManager(models.Manager):

    def add_member(self, email, project):
        user = User.objects.filter(email__contains=email)
        import pdb; pdb.set_trace();

        if not user.exists():
            return

        project.user_ids.add(user.get().id)
        return True


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


class List(models.Model):

    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TaskManager(models.Manager):

    def get_index(self, current_list):
        index = 0
        if current_list.task_set.all().count() > 0:
            index = current_list.task_set.all().reverse()[0].index + 1

        next_tasks = Task.objects.filter(index__gte=index)
        next_tasks.update(index=F('index') + 1)

        return index

    def _format_value(self, value):
        if isinstance(value, float) or isinstance(value, int):
            hours, minutes = divmod(abs(value) * 60, 60)
            minutes = round(minutes)
            if minutes == 60:
                minutes = 0
                hours += 1

            if value < 0:
                return '-%02d:%02d' % (hours, minutes)
        return '%02d:%02d' % (hours, minutes)

    def update_order_task(self, datas):
        for data in datas:
            current_task = Task.objects.get(id=data['task_id'])
            current_task.project_list = List.objects.get(id=data['list_id'])
            current_task.index = data['index']
            current_task.save()


class Task(models.Model):

    name = models.CharField(max_length=120)
    description = models.TextField()
    project_list = models.ForeignKey(List, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    deadline = models.DateField(blank=True, null=True)
    index = models.IntegerField(db_index=True)
    planned_hours = models.FloatField(default=0)
    effective_hours = models.FloatField(default=0)
    remaining_hours = models.FloatField(default=0)

    objects = models.Manager()
    objects_task = TaskManager()

    @property
    def planned_hours_time(self):
        return Task.objects_task._format_value(self.planned_hours)

    @property
    def effective_hours_time(self):
        timesheets = self.timesheet_set.all()
        total_effective_hours = sum(timesheet.unit_hour for timesheet in timesheets)
        return Task.objects_task._format_value(total_effective_hours)

    @property
    def remaining_hours_time(self):
        timesheets = self.timesheet_set.all()
        total_effective_hours = sum(timesheet.unit_hour for timesheet in timesheets)
        remaining_hours = self.planned_hours - total_effective_hours

        return Task.objects_task._format_value(remaining_hours)

    class Meta:
        ordering = ['index']
