from django import forms
from .models import Attendance

class AttendanceForm(forms.ModelForm):

    class Meta:

        model = Attendance

        fields = [
            'employee',
            'status',
            'check_in_time'
        ]

        widgets = {

            'check_in_time': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': 'form-control'
                }
            )
        }