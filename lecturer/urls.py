
from django.conf.urls import url
from . import views


app_name = 'lecturer'
urlpatterns = [
    url(r'^$', views.front_page, name='front_page'),
    url(r'^login', views.login, name='login_page'),
]
