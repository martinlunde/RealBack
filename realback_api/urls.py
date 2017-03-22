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
        url(r'^questions/(?P<question_id>[0-9]+)/', include([

            url(r'^vote/$', api.LectureQuestionVotes.as_view(), name='lecture_question_votes'),

        ])),
        url(r'^pace/$', api.LecturePace.as_view(), name='lecture_pace'),
        url(r'^volume/$', api.LectureVolume.as_view(), name='lecture_volume'),
        url(r'^topics/$', api.LectureTopics.as_view(), name='lecture_topics'),
        url(r'^topics/(?P<topic_id>[0-9]+)/', include([

            url(r'^$', api.LectureTopicDetails.as_view(), name='lecture_topic_details'),
            url(r'^understanding/$', api.LectureTopicUnderstanding.as_view(), name='lecture_topic_understanding'),

        ])),

    ])),
    url(r'^courses/$', api.Courses.as_view(), name='courses'),
    url(r'^courses/(?P<course_id>[0-9]+)/', include([

        url(r'^$', api.CourseDetails.as_view(), name='course_details'),
        url(r'^lectures/$', api.CourseLectures.as_view(), name='course_lectures'),
        url(r'^stats/', api.LectureStats.as_view(), name='stats'),
    ])),
]
