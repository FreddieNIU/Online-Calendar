from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.

class addEventForm(forms.Form):
    event = forms.CharField(help_text="Enter the event title")
    date = forms.DateField(help_text="Enter the date.")
    start_time = forms.TimeField(help_text="Enter the start time of the event.")
    end_time = forms.TimeField(help_text="Enter the end time of the event.")

    def clean_renewal_date(self):
        event = self.cleaned_data['event']
        date = self.cleaned_data['date']
        start = self.cleaned_data['start_time']
        end = self.cleaned_data['end_time']

        # if date < datetime.date(2021,1,1) or date > datetime.date(2021,1,31):
        #
        #     raise ValidationError(_('Invalid date - please give a date in the range of 2020-01'))
        #
        # if end < start:
        #     raise ValidationError(_('Invalid timeslot - event ending time is earlier than the event start time.'))

        return event,date,start,end

