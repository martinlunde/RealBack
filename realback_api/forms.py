
from django import forms
from . import models


class QuestionForm(forms.ModelForm):
    class Meta:
        model = models.Question
        fields = ['text']
        widgets = {'text': forms.Textarea()}


class CourseForm(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = ['title']


class LectureForm(forms.ModelForm):
    class Meta:
        model = models.Lecture
        fields = ['title']


class LectureTopicForm(forms.ModelForm):
    class Meta:
        model = models.LectureTopic
        fields = ['title', 'order']


class TopicUnderstandingForm(forms.Form):
    understanding = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'style': 'display: none;'})
    )


class PaceForm(forms.Form):
    pace = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'style': 'display: none;'})
    )


class VolumeForm(forms.Form):
    volume = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'style': 'display: none;'})
    )


class RatingForm(forms.Form):
    rating = forms.IntegerField(required=True)
