"""
URL's belonging to the lecturer application
"""

from django.conf.urls import url, include
from . import views, api


app_name = 'lecturer'
urlpatterns = [
    url(r'^$', views.create_lecture_in_course, name='front_page'),
    # skal et inni lecturer/course eller lecturer?
    url(r'^(?P<course>[\s\S]*)/(?P<lecture>[\s\S]*)$', views.lecture, name='lecture'),
    url(r'^(?P<course>[\s\S]*)$', views.course, name='course'),

    # API URLs
    url(r'^lectures/(?P<pin>[A-Z0-9]{6})/', include([

        url(r'^$', api.lecture_details, name='api-lecture_details'),
        url(r'^questions/$', api.LectureQuestions.as_view(), name='api-lecture_questions'),
        url(r'^speed/$', api.LectureSpeed.as_view(), name='api-lecture_speed'),

    ])),
    url(r'^courses/(P<)')
    # TODO soundlevel
]
