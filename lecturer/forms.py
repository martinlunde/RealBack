
from django import forms
from . import models


class NewOverallForm(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = ['title']
