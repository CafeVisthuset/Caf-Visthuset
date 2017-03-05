from django.shortcuts import render, redirect
from django.http.response import HttpResponse, HttpResponseRedirect
from .models import Booking, Bike, LunchBooking, calc_booking_no
from .forms import CreateAvailableBikeForm
from datetime import datetime, timedelta, date
from django.forms.formsets import formset_factory
from database.forms import BaseCreateAvailableBikeFormset, BookingForm
from django.contrib.admin.views.decorators import staff_member_required
from database.models import BikeAvailable, BikeExtra, Guest, Lunch
from django.utils.safestring import mark_safe
from database.calendars import BikeCalendar
from database.serializers import BikeBookingSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth.models import User
from time import strftime
from database.helperfunctions import setInput
from django.urls.base import reverse
from database.admin import BikesAvail

def index(request):
    latest_booking_list = Booking.objects.order_by('-BookingDate')[:5]
    output = ', '.join([q.guest for q in latest_booking_list])
    return HttpResponse(output)

def ThanksView(request):
    return HttpResponse('Tack för din bokning!')

def booking(request, booking):
    response = "You're looking at booking %s."
    return HttpResponse(response % booking)
  
def perdelta(start, end, delta):
    curr = start
    while curr <= end:
        yield curr
        curr += delta
    
def trial(request):
    today = datetime.today()
    
    output = today.strftime(format)
    return HttpResponse(output)

@staff_member_required
def create_available_bikes(request):
    # Formset for creating bikes
    CreateAvailableBikeFormset = formset_factory(CreateAvailableBikeForm,
                                                 formset=BaseCreateAvailableBikeFormset,
                                                 extra=len(Bike.objects.all()),
                                                 max_num=25,
                                                 )
    if request.method == 'POST':
        formset = CreateAvailableBikeFormset(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset:
                data = form.cleaned_data
                if data['bike'] is not None:
                    start = data['from_date']
                    numdays = data['to_date'].day - start.day
                    date_list = [(start + timedelta(days=x)) for x in range(0,numdays + 1)]
                
                    # Create available bike
                    if data['action'] == 'create':
                        for day in date_list:
                            # See if object is already created
                            try:
                                BikeAvailable.objects.get(
                                    bike = data['bike'],
                                    available_date = day)
                            # Create a new object if try fails    
                            except:
                                BikeAvailable.objects.create_available_bike(
                                    bike=data['bike'],
                                    date=day)
                
                    # Delete available bike
                    elif data['action'] == 'delete':
                        bk = BikeAvailable.objects.filter(
                                bike = data['bike'],
                                available_date__gte = start).filter(
                                    bike = data['bike'],
                                available_date__lte = data['to_date'])
                        bk.delete()

                        
                        
    else:
        formset = CreateAvailableBikeFormset()
        
    # Calendar
    today = datetime.now()
    my_bikes = BikeAvailable.objects.all().order_by('available_date')
    calendar = BikeCalendar(my_bikes).formatmonth(today.year, today.month)
    '''
    TODO:
    # Make sure no two same available bikes can be created. For instance via unique together
    # create calendar for bikes
    '''
    
    return render(request, 'bookings/create_available_bikes.html',
                  {'formset': formset,
                   'calendar': mark_safe(calendar),
                   })


def BookBikeView(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        data = form.cleaned_data
        print(data)
        response_data = data
        return render(request, 'bookings/test.html', {'data': response_data})
    else:
        response_data = 'get' #BikeAvailable.objects.all()
        form = BookingForm
    return render(request, 'bookings/booking.html',{'message': response_data, 'form': form})

class BikeBookingResponse(APIView):
    '''
    View with responses for Bike Booking
    
    More docs...
    '''
    renderer_classes = [TemplateHTMLRenderer]
    
    def get(self, request):
        '''
        returns an empty form from the serializer
        '''
        initial = {
            'first_name': '',
            'start_date': date.today(),
            'duration': timedelta(days=1),
            'adult_bikes': 2,
            'child_bikes': 0,
            'extras': BikeExtra.objects.all(),
            'vegetarian_lunches': 0,
            'meat_lunches': 0,
            'fish_lunches': 0,
            'last_name': '',
            'phone_number': '',
            'email': '',
            'newsletter': True,
            'other': '',
            }
        serializer = BikeBookingSerializer(initial)
        return Response({'serializer': serializer}, template_name='bookings/booking.html')
    
    def post(self, request):
        '''
        Creates a new bikes booking if all fields are filled in correctly, otherwise return the
        same form again with error messages
        '''
        serializer = BikeBookingSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.data)
            # Structure incoming data
            #Guest data
            first_name = setInput(serializer, 'first_name')
            last_name= setInput(serializer, 'last_name')
            email = setInput(serializer, 'email')
            phone_number = setInput(serializer, 'phone_number')
            newsletter = setInput(serializer, 'newsletter')
            
            # Dates and times
            start_date = datetime.strptime(setInput(serializer, 'start_date'), '%Y-%m-%d')
            duration = setInput(serializer, 'duration')
            
            # Bike information
            adult_bikes = setInput(serializer, 'adult_bikes')
            child_bikes = setInput(serializer, 'child_bikes')
            extras = setInput(serializer, 'extras')
            
            # Lunch information
            veg = setInput(serializer, 'vegetarian_lunches')
            meat = setInput(serializer, 'meat_lunches')
            fish = setInput(serializer, 'fish_lunches')
            
            # Other booking info
            other = setInput(serializer, 'other')
            
            # Get or create guest
            guest = Guest.objects.post_get_or_create(first_name, last_name, email,
                kwargs={'phone_number': phone_number, 'newsletter': newsletter})
            
            print(guest)
            # Create booking
            end_date = start_date + duration - timedelta(days=1)
            number_of_guests = adult_bikes + child_bikes
            
            booking = Booking.book.create_booking(guest=guest,
                                             start_date=start_date,
                                             end_date=end_date,
                                             numberOfGuests=number_of_guests, 
                                             special_requests=other)
            print(booking, type(booking))
            # Book bikes
            included_bikes = {}
            if adult_bikes != 0:
                booking.book.setBikeBooking('adult', adult_bikes, start_date, duration)
                '''
                found_a, adult_bike_list = BikeAvailable.objects.find_and_book_bikes(
                    adult_bikes, start_date, duration, booking.booking, 'adult')
                print(found_a, adult_bike_list)
                '''
                included_bikes['Vuxencyklar'] = adult_bikes
            
            if child_bikes !=0:
                found_c, child_bike_list = BikeAvailable.objects.find_and_book_bikes(
                    adult_bikes, start_date, duration, booking.booking, 'child')
                print(found_c, child_bike_list)
                included_bikes['Barncyklar'] = child_bikes
            
            
            
            return 
            # Book extras
            included_bikes['Tillbehör'] = extras
            # Book lunches
            included_lunches = {}
            if veg != 0 and veg is not None:
                LunchBooking.objects.create(type=Lunch.objects.get(type='vegetarian'), day=start_date,
                                            quantity=veg, booking=booking)
                included_lunches['Vegetarisk'] = veg
            
            if meat != 0 and meat is not None:
                LunchBooking.objects.create(type=Lunch.objects.get(type='meat'), day=start_date,
                                            quantity=meat, booking=booking)
                included_lunches['Kallskuret'] = meat
                
            if fish != 0 and fish is not None:
                LunchBooking.objects.create(type=Lunch.objects.get(type='fish'), day=start_date,
                                            quantity=fish, booking=booking)
                included_lunches['Fisk'] = fish
                
            
            # Saves the booking and updates prices
            booking.save()
             
            # What to send back to the view
            message = mark_safe(
            ''' <h1>Tack {0} för din bokning!</h1><br>
            
            Du startar den {1} och reser hem igen den {2}. </br>
            
            I din bokning ingår följande:
            '''.format(first_name, start_date.strftime('%d %B %Y'), end_date.strftime('%d %B %Y')))
            
            return redirect('confirmation', **{'message': message,
                             'included_lunches': included_lunches,
                             'included_bikes': included_bikes,
                             'booking_number': booking.booking},)
                            #template_name='bookings/confirmation.html'))
        
        # if form is not correctly filled in
        print(False)
        return Response({'serializer': serializer,
                         'message': 'Alla fält måste vara korrekt ifyllda!'},
                        template_name='bookings/booking.html')
        
def confirmation(request, **kwargs):
    
    return render(request, 'bookings/confirmation.html', {'message': kwargs['message']})
    