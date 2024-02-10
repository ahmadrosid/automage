from django import forms
from .models import CronJob

class CronJobForm(forms.ModelForm):
    class Meta:
        model = CronJob
        fields = ['name', 'command', 'schedule']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CronJobForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(CronJobForm, self).save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance
