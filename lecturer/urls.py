
from django.conf.urls import url
from . import views


app_name = 'lecturer'
urlpatterns = [
    url(r'^$', views.front_page, name='front_page'),
    # url(r'^login$', views.login, name='login_page'),
    url(r'^lecture/new$', views.new_lecture, name='new_lecture'),
    url(r'^course/new$', views.new_course, name='new_course'),
]
