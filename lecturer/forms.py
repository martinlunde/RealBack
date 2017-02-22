
from django import forms
from . import models


class NewCourseForm(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = ['title', 'description']


class NewLectureForm(forms.ModelForm):
    class Meta:
        model = models.Lecture
        fields = ['title', 'description']
