"""
URL's belonging to the RealBack API application
"""

from django.conf.urls import url, include
from . import api


app_name = 'api'
urlpatterns = [
    url(r'^lectures/(?P<pin>[A-Z0-9]{6})/', include([

        url(r'^$', api.LectureDetails.as_view(), name='lecture_details'),
        url(r'^join/$', api.LectureDetails.as_view(), {'join': True}, name='lecture_join'),
        url(r'^leave/$', api.LectureLeave.as_view(), name='lecture_leave'),
        url(r'^questions/$', api.LectureQuestions.as_view(), name='lecture_questions'),
        url(r'^questions/(?P<question_id>[0-9]+)/', include([

            url(r'^vote/$', api.LectureQuestionVotes.as_view(), name='lecture_question_votes'),
            url(r'^active/$', api.QuestionActive.as_view(), name='question_active'),

        ])),
        url(r'^pace/$', api.LecturePace.as_view(), name='lecture_pace'),
        url(r'^volume/$', api.LectureVolume.as_view(), name='lecture_volume'),
        url(r'^timer/$', api.LectureTimer.as_view(), name='lecture_timer'),
        url(r'^start_timer/$', api.StartTimer.as_view(), name='start_timer'),
        url(r'^stop_timer/$', api.StopTimer.as_view(), name='stop_timer'),
        url(r'^reset_rating/$', api.ResetRating.as_view(), name='reset_rating'),
        url(r'^rate/$', api.Rate.as_view(), name='rate'),
        url(r'^topics/$', api.LectureTopics.as_view(), name='lecture_topics'),
        url(r'^topics/(?P<topic_id>[0-9]+)/', include([

            url(r'^$', api.LectureTopicDetails.as_view(), name='lecture_topic_details'),
            url(r'^understanding/$', api.LectureTopicUnderstanding.as_view(), name='lecture_topic_understanding'),

        ])),
        url(r'^reset/', include([

            url(r'^volume/$', api.LectureResetVolume.as_view(), name='lecture_reset_volume'),
            url(r'^pace/$', api.LectureResetPace.as_view(), name='lecture_reset_pace'),

        ])),

    ])),
    url(r'^courses/$', api.Courses.as_view(), name='courses'),
    url(r'^courses/(?P<course_id>[0-9]+)/', include([

        url(r'^$', api.CourseDetails.as_view(), name='course_details'),
        url(r'^lectures/$', api.CourseLectures.as_view(), name='course_lectures'),
        url(r'^stats/', api.LectureStats.as_view(), name='stats'),
    ])),
]
