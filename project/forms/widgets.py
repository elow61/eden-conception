from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError


class HourWidget(widgets.TextInput):

    def _format_value(self, value):
        if isinstance(value, float) or isinstance(value, int):
            import math

            hours = math.floor(value)
            minutes = (value - hours) * 60
            value = f'{int(hours):02d}:{int(minutes):02d}'

        return value

    def render(self, name, value, attrs=None, renderer=None):
        value = self._format_value(value)
        return super(HourWidget, self).render(name, value, attrs)

    def _has_changed(self, initial, data):
        return super(HourWidget, self)._has_changed(self._format_value(initial), data)


class HourField(forms.Field):
    widget = HourWidget

    def clean(self, value):
        super(HourField, self).clean(value)

        import re
        match = re.match("^([0-9]{1,2}):([0-9]{2})$", value)
        if not match:
            raise ValidationError("Please enter a valid hour ( ex: 12:34 )")

        groups = match.groups()
        hour = float(groups[0])
        minutes = float(groups[1])

        if minutes >= 60:
            raise ValidationError("Invalid value for minutes")

        return hour + minutes / 60
