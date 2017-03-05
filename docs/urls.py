'''
Created on 16 okt. 2016

@author: Adrian
'''
from django.conf.urls import url
from . import views

app_name = 'docs'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name = 'Index'),
    url(r'^tutor/', views.tutor, name='Tutor'),
]