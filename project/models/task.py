''' The model Task and his manager '''
from django.db import models
from django.db.models import F
from project.models.list import List
from user.models import User


class TaskManager(models.Manager):
    ''' The manager for the model task. '''

    def get_index(self, current_list):
        ''' Method to get the order position into the project.
            If we have many lists, the first task will be into
            the first list at the first position.

            If we supposed to have 2 task into the first list and
            3 tasks into the second list, the first task of second
            list have the index 3.

            Example with i = index :

            backlog      |  To Do
            ------------ | ------------
            task (i = 1) | task (i = 3)
            task (i = 2) | task (i = 4)
        '''
        index = 0
        if current_list.task_set.all().count() > 0:
            index = current_list.task_set.all().reverse()[0].index + 1

        next_tasks = Task.objects.filter(index__gte=index)
        next_tasks.update(index=F('index') + 1)

        return index

    def _format_value(self, value):
        ''' This method convert a float into an hour.
            Used to the next fields :
            - planned_hours
            - effective_hours
            - remaining_hours
        '''
        if isinstance(value, (float, int)):
            hours, minutes = divmod(abs(value) * 60, 60)
            minutes = round(minutes)
            if minutes == 60:
                minutes = 0
                hours += 1

            if value < 0:
                return f'-{int(hours):02d}:{int(minutes):02d}'
        return f'{int(hours):02d}:{int(minutes):02d}'

    def update_order_task(self, datas):
        ''' When drag and drop a task into a list, we update
            his order (his index).
        '''
        for data in datas:
            current_task = Task.objects.get(id=data['task_id'])
            current_task.project_list = List.objects.get(id=data['list_id'])
            current_task.index = data['index']
            current_task.save()


class Task(models.Model):
    ''' the model task to have tasks into lists of projects '''
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
        ''' class to ordering the model task '''
        ordering = ['index']
