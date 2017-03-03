"""
URL's belonging to the lecturer application
"""

from django.conf.urls import url, include
from . import api


app_name = 'api'
urlpatterns = [
    # API URLs
    url(r'^lectures/$', api.Lecture.as_view(), name='lecture'),
    url(r'^lectures/(?P<pin>[A-Z0-9]{6})/', include([

        url(r'^$', api.LectureDetails.as_view(), name='lecture_details'),
        url(r'^questions/$', api.LectureQuestions.as_view(), name='lecture_questions'),
        url(r'^speed/$', api.LectureSpeed.as_view(), name='lecture_speed'),
        # TODO soundlevel

    ])),
    url(r'^courses/$', api.Course.as_view(), name='course'),
    url(r'^courses/(P<course_id>[0-9]+)/', include([

        url(r'^$', api.CourseDetails.as_view(), name='course_details'),

    ])),
]
