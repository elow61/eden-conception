''' Forms for the model Timesheet '''
from django.forms import ModelForm, DateField
from timesheet.models.timesheet import Timesheet
from project.forms.widgets import HourField


class UpdateTimesheetForm(ModelForm):
    ''' Form to update the timesheets or create into a task '''
    created_at = DateField(input_formats=['%d/%m/%Y'], required=True)

    def __init__(self, *args, **kwargs):
        super(UpdateTimesheetForm, self).__init__(*args, **kwargs)
        self.fields['unit_hour'] = HourField()

    class Meta:
        ''' Is used to target the model and her field '''
        model = Timesheet
        fields = ['created_at', 'user', 'description', 'unit_hour']
