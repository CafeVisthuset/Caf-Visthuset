'''
Created on 16 okt. 2016

@author: Adrian
'''
from django.conf.urls import url
from . import views, calendars

app_name = "database"
urlpatterns = [
    # /bookings/
    url(r'^availablebike/$', views.create_available_bikes, name='createbikes'),
    url(r'^bookingcal/$', views.booking_calendar, name='bookingcalendar'),
    url(r'^viewbookings/$', views.view_bookings, name='bookings_today'),
    # /bookings/bookingNo/
    url(r'^calendar/$', calendars.calendar, name='eventcalendar'),
    url(r'^bikebooking/', views.customer_bike_booking_view, name='bike_booking'),
    url(r'^package/$', views.package_display, name='package_list'),
    url(r'^package/(?P<slug>[a-z]+)/', views.package_booking, name='package'),
    url(r'^(?P<pk>[0-9]+)/thanks/$', views.confirmation_view, name='confirmation'),
    #url(r'^(?P<booking>[0-9]+)/$', views.ViewBooking.as_view(), name='booking-detail')
    ]
#views.BikeBookingResponseView.as_view()    ]
