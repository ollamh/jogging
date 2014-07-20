from django import forms

import timedelta

from .models import JoggingEntry

class JoggingEntryForm(forms.ModelForm):
    """
    Entry Form
    """
    form_name = 'entry_form'
    duration = timedelta.forms.TimedeltaFormField()

    def __init__(self, *args, **kwargs):
        kwargs.update(scope_prefix='entry')
        super(JoggingEntryForm, self).__init__(*args, **kwargs)

    class Meta:
        model = JoggingEntry
        fields = ('date', 'duration', 'distance')
