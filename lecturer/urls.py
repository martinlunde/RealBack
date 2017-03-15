"""
URL's belonging to the lecturer application
"""

from django.conf.urls import url
from . import views


app_name = 'lecturer'
urlpatterns = [
    url(r'^$', views.front_page, name='front_page'),

]
