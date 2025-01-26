from django import forms
from .models import TrainerSchedule

class TrainerScheduleForm(forms.ModelForm):
    class Meta:
        model = TrainerSchedule
        fields = ['datetime_start', 'datetime_end']
        widgets = {
            'datetime_start': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'datetime_end': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
