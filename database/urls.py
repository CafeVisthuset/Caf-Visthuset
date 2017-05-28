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
    url(r'^calendar/$', calendars.calendar, name='eventcalendar'),
    url(r'^bikebooking/', views.customer_bike_booking_view, name='bike_booking'),
    url(r'^package/(?P<slug>[a-z]+)/', views.package_booking, name='package_booking'),
    url(r'^(?P<pk>[0-9]+)/thanks/$', views.confirmation_view, name='confirmation'),
    ]
#views.BikeBookingResponseView.as_view()    ]
