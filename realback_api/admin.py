
from django.contrib import admin
from .models import Lecture, Course, Question, LectureTopic


admin.site.register(Lecture)
admin.site.register(Course)
admin.site.register(Question)
admin.site.register(LectureTopic)
