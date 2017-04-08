'''
Created on 16 okt. 2016

@author: Adrian
'''
from django.conf.urls import url
from . import views, calendars

app_name = "database"
urlpatterns = [
    # /bookings/
    url(r'^$', views.index , name="index"),
    url(r'^availablebike/$', views.create_available_bikes, name='createbikes'),
    # /bookings/bookingNo/
    url(r'^(?P<booking_id>[0-9]+)/$', views.booking, name='booking'),
    #url(r'^accomodation/', views.AccomodationBookingView.as_view()),
    #url(r'^bikes/', views.BikeBookingView, name='bikebooking'),
    url(r'^test/', views.trial),
    url(r'^calendar/$', calendars.calendar, name='eventcalendar'),
    url(r'^bikebooking/', views.BikeBookingResponse.as_view(), name='bike_booking'),
    url(r'^(?P<pk>[0-9]+)/thanks/$', views.confirmation_view, name='confirmation'),
    ]