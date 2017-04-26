"""VisthusetAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from VisthusetAPI.views import *
from rest_framework import routers
from Economy.views import UserViewSet
import database.views as booking
import VisthusetAPI

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    # Visthuset urls
    url(r'^$', IndexView, name="visthuset_index"),
    url(r'^menu/$', MenuView.as_view(), name="menu"),
    url(r'^calendar/$', CalendarView.as_view(), name="calendar"),
    url(r'^events/', include('events.urls')),
    url(r'^about/$', AboutView.as_view(), name="about"),
    url(r'^contact/$', ContactView.as_view(), name="contact"),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    
    # API urls
    url(r'^api/$', APIIndexView.as_view(), name="api_index"),
    url(r'^admin/', admin.site.urls),
    url(r'^cleaning/', include('cleaning.urls')),
    url(r'^economy/', include('Economy.urls')),
    url(r'^booking/', include('database.urls')),
    url(r'^docs/', include('docs.urls')),
    url(r'^root/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/availablebike/$', booking.create_available_bikes, name='createbikes'),
]