
from django import forms
from realback_api import models


class NewOverallForm(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = ['title']
