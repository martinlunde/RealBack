
from django import forms
from . import models


class QuestionForm(forms.ModelForm):
    class Meta:
        model = models.Question
        fields = ['text']

class CourseForm(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = ['title']
