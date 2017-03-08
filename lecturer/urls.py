"""
URL's belonging to the lecturer application
"""

from django.conf.urls import url
from . import views


app_name = 'lecturer'
urlpatterns = [
    url(r'^$', views.create_lecture_in_course, name='front_page'),
    # skal et inni lecturer/course eller lecturer?
    url(r'^(?P<course>[\s\S]*)/(?P<lecture>[\s\S]*)$', views.lecture, name='lecture'),
    url(r'^(?P<course>[\s\S]*)$', views.course, name='course'),

]
