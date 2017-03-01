
from django.conf.urls import url
from . import views


app_name = 'lecturer'
urlpatterns = [
    url(r'^$', views.create_lecture_in_course, name='front_page'),
    # url(r'^login$', views.login, name='login_page'),
    # skal et inni lecturer/course eller lecturer?
    url(r'^(?P<course>[\s\S]*)/(?P<lecture>[\s\S]*)$', views.lecture, name='lecture'),
    url(r'^(?P<course>[\s\S]*)$', views.course, name='course'),
]
