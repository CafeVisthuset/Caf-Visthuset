'''
Created on 31 okt. 2016

@author: Adrian
'''
from django.conf.urls import url

from . import views


app_name = 'cleaning'
urlpatterns = [
    # ex: /cleaning/
    url(r'^$', views.CleanIndexView, name='CleanIndex'),
    url(r'^thanks/', views.Results),
    ]