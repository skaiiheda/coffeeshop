from datetime import datetime

from django import forms
from .models import Attendance, Shift
from datetime import datetime
from croniter import croniter
from django.forms import ModelForm, ValidationError

# class ShiftCreateForm(forms.ModelForm):
#     class Meta:
#         model = Attendance
#         fields = ['shift']


class ShiftCreateForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['shift']

    def __init__(self, *args, **kwargs):
        employee_id = kwargs.pop('employee_id')
        shift_id = kwargs.pop('shift_id')
        super().__init__(*args, **kwargs)
        self.fields['shift'] = forms.ModelChoiceField(queryset=Shift.objects.filter(employee_id=employee_id, id=shift_id))
