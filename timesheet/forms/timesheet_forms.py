from django.forms import ModelForm, DateField
from django.utils.translation import gettext_lazy as _
from timesheet.models.timesheet import Timesheet
from project.forms.widgets import HourField


class UpdateTimesheetForm(ModelForm):

    created_at = DateField(input_formats=['%d/%m/%Y'], required=True)

    def __init__(self, *args, **kwargs):
        super(UpdateTimesheetForm, self).__init__(*args, **kwargs)
        self.fields['unit_hour'] = HourField()

    class Meta:
        model = Timesheet
        fields = ['created_at', 'user', 'description', 'unit_hour']
