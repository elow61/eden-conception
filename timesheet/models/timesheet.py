from django.db import models
from project.models.task import Task
from user.models import User


class TimesheetManager(models.Manager):

    def _format_value(self, value):
        if isinstance(value, float) or isinstance(value, int):
            hours, minutes = divmod(abs(value) * 60, 60)
            minutes = round(minutes)
            if minutes == 60:
                minutes = 0
                hours += 1

            if value < 0:
                return f'-{int(hours):02d}:{int(minutes):02d}'

            return f'{int(hours):02d}:{int(minutes):02d}'


class Timesheet(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    description = models.CharField(max_length=200)
    unit_hour = models.FloatField(default=0)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    objects = models.Manager()
    objects_timesheet = TimesheetManager()

    @property
    def unit_hour_time(self):
        return Timesheet.objects_timesheet._format_value(self.unit_hour)
