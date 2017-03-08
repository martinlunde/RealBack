"""
URL's belonging to the RealBack API application
"""

from django.conf.urls import url, include
from . import api


app_name = 'api'
urlpatterns = [
    url(r'^lectures/(?P<pin>[A-Z0-9]{6})/', include([

        url(r'^$', api.LectureDetails.as_view(), name='lecture_details'),
        url(r'^questions/$', api.LectureQuestions.as_view(), name='lecture_questions'),
        url(r'^speed/$', api.LectureSpeed.as_view(), name='lecture_speed'),
        # TODO soundlevel

    ])),
    url(r'^courses/$', api.Courses.as_view(), name='courses'),
    url(r'^courses/(P<course_id>[0-9]+)/', include([

        url(r'^$', api.CourseDetails.as_view(), name='course_details'),
        url(r'^lectures/$', api.CourseLectures.as_view(), name='course_lectures'),

    ])),
]
