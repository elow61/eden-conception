""" All views for the user application """
from django.forms import inlineformset_factory
from django.views import View

from project.models.task import Task
from timesheet.models.timesheet import Timesheet
from timesheet.forms.timesheet_forms import UpdateTimesheetForm


class TimesheetView(View):

    @classmethod
    def update_timesheet(cls, request):
        TimeFormSet = inlineformset_factory(
            parent_model=Task,
            model=Timesheet,
            form=UpdateTimesheetForm,
            can_delete=True,
        )
        current_task = Task.objects.get(id=request.POST.get('task_id'))
        formset = TimeFormSet(request.POST, instance=current_task)
        if formset.is_valid():
            formset.save()
