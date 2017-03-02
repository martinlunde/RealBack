"""
URL's belonging to the attendee application
"""

from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about_us/', views.about_us, name='about'),

]
