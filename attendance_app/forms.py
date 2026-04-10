from django import forms
from students.models import Student, CLASS_CHOICES, SECTION_CHOICES
from .models import Attendance
import datetime


class AttendanceFilterForm(forms.Form):
    student_class = forms.ChoiceField(choices=[('', 'All Classes')] + CLASS_CHOICES,
                                      required=False,
                                      widget=forms.Select(attrs={'class': 'form-select'}))
    section = forms.ChoiceField(choices=[('', 'All Sections')] + SECTION_CHOICES,
                                required=False,
                                widget=forms.Select(attrs={'class': 'form-select'}))
    date = forms.DateField(initial=datetime.date.today,
                           widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))


class QRSessionForm(forms.Form):
    student_class = forms.ChoiceField(choices=CLASS_CHOICES,
                                      widget=forms.Select(attrs={'class': 'form-select'}))
    section = forms.ChoiceField(choices=SECTION_CHOICES,
                                widget=forms.Select(attrs={'class': 'form-select'}))
    date = forms.DateField(initial=datetime.date.today,
                           widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
