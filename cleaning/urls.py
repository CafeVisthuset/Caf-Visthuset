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
    url(r'^fridge/', views.FridgeControlView.as_view()),
    url(r'^freezer/', views.FreezerControlView.as_view()),
    url(r'^clean/', views.FrigdeView.as_view()),
    url(r'^thanks/', views.Results),
    ]