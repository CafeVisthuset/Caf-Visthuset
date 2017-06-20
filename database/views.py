from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from .forms import CreateAvailableBikeForm, ChildBikeBookingForm, ChildBikeFormset
from datetime import datetime, timedelta, date
from django.forms.formsets import formset_factory
from database.forms import BaseCreateAvailableBikeFormset, CustomerBikeBookingForm,\
    CustomerPackageBookingForm
from django.contrib.admin.views.decorators import staff_member_required
from database.models import *
from django.utils.safestring import mark_safe
from database.calendars import BikeCalendar, BookingsCalendar
from database.helperfunctions import create_date_list
from docs.models import EmailTexts
from django.core.mail import send_mail
from django.template import Template, Context
from docs.models import Page, PageContent
from django.views.generic.detail import DetailView

def perdelta(start, end, delta):
    curr = start
    while curr <= end:
        yield curr
        curr += delta

@staff_member_required
def create_available_bikes(request):
    # Formset for creating bikes
    CreateAvailableBikeFormset = formset_factory(CreateAvailableBikeForm,
                                                 formset=BaseCreateAvailableBikeFormset,
                                                 extra=1,
                                                 max_num=25,
                                                 )
    if request.method == 'POST':
        formset = CreateAvailableBikeFormset(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset:
                data = form.cleaned_data
                start = data['from_date']
                numdays = data['to_date'].day - start.day
                date_list = [(start + timedelta(days=x)) for x in range(0,numdays + 1)]
                
                if data['bike'] is not None:
                    # Create available bike
                    if data['action'] == 'create':
                        for day in date_list:
                            BikeAvailable.objects.get_or_create(
                                    bike = data['bike'],
                                    available_date = day)

                    # Delete available bike
                    elif data['action'] == 'delete':
                        bk = BikeAvailable.objects.filter(
                                bike = data['bike'],
                                available_date__gte = start).filter(
                                    bike = data['bike'],
                                available_date__lte = data['to_date'])
                        bk.delete()
                else:
                    if data['action'] == 'all':
                        print('all')
                        for bike in Bike.objects.all():
                            for day in date_list:
                                BikeAvailable.objects.get_or_create(
                                        bike=bike,
                                        available_date = day)
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

def customer_bike_booking_view(request):
    # Get page text data from database
    pagename = 'uthyrning'
    page = Page.objects.get(code=pagename)
    texts = PageContent.objects.filter(page__code = pagename, publish=True).order_by('order')
    
    # Form data and handling
    if request.method == 'POST':
        form = CustomerBikeBookingForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # Time variables
            start_date = data['start_date']
            duration = data['duration']
            end_date = start_date + duration - timedelta(days=1)
            date_list = create_date_list(start_date, duration.days)
            
            # Build bike dictionary
            bikes = {'adult': data['adult_bikes'], 'young': data['young_bikes'], 
                     'child': data['child_bikes'], 'smallChild': data['small_child_bikes']}
            
            # Count number of bikes
            number_of_adults = data['adult_bikes']
            number_of_children = (int(data['small_child_bikes']) + int(data['child_bikes']) + 
                                  int(data['young_bikes']))
            # Messages
            biketype_dict = {'adult': 'vuxencykel', 'young': 'ungdomscykel', 'child': 'barncykel',
                    'smallChild': 'småbarncykel'}
            
            bike_list = []
            for biketype, amount in bikes.items():
                if amount is not None and amount > 0:
                    success, list = (BikeAvailable.objects.
                                            get_available_bikes_for_dates(biketype,
                                                                          amount,
                                                                          start_date,
                                                                          end_date,
                                                                          duration))
                    if success:
                        bike_list += list
                    else:
                        return render(request, 'bookings/bike_booking.html', {'form': form,
                                                                              'page': page,
                                                                              'texts': texts,
                                                                              'message': mark_safe('''
                                         Det verkar som att vi inte har tillräckligt många {} lediga<br>
                                         för en eller flera av de önskade dagarna. Ring oss gärna på<br>
                                         0506 - 77 75 50 eller skicka ett mejl till <a href="mailto:info@cafevisthuset.se">
                                         info@cafevisthuset.se</a> så kanske vi kan hjälpa till.
                                         '''.format(biketype_dict[biketype]))})
            # Get or create guest
            guest = Guest.objects.post_get_or_create(data['first_name'],
                                                     data['last_name'],
                                                     data['email'],
                                                     kwargs={'phone_number': data['phone_number'],
                                                             'newsletter': data['newsletter']})
            # Create booking
            booking = Booking.objects.create(guest=guest,
                                          start_date=start_date,
                                          end_date=end_date,
                                          adults=number_of_adults,
                                          children=number_of_children,
                                          status='actv',
                                          special_requests=data['other'])
            # Book bikes
            # bike booking not used, but can be used for debugging
            success, bike_booking = booking.setBikeBooking(bike_list, start_date, end_date, duration)
            
            # Should not happen
            if not success:
                '''
                TODO:
                # Implement report if something goes wrong and send an email to us. 
                '''
                return render(request, 'failed.html')
            '''
            TODO:
            # Implement booking of bike extras to 
            '''
            # Build lunch dictionary
            lunches ={'veg': data['veg_lunch'], 'fish': data['fish_lunch'], 'meat': data['meat_lunch']}
            # Book lunches
            for lunchtype, amount in lunches.items():
                if amount > 0:
                    LunchBooking.objects.create(
                            type=Lunch.objects.get(type=lunchtype), 
                            day=start_date,
                            quantity=amount,
                            booking=booking)
            
            # Saves the booking and updates prices
            booking.save()
            return redirect('database:confirmation', pk = booking.booking)
            
    else:
        form = CustomerBikeBookingForm()
        
    return render(request, 'bookings/bike_booking.html', {'form': form, 'page':page, 'texts':texts})  

@staff_member_required
def booking_calendar(request):
    today = datetime.today()
    bookings = BikesBooking.objects.all().order_by('from_date').exclude(bike=None)
    calendar = BookingsCalendar(bookings).formatmonth(year=today.year, month=5)
    return render(request, 'bookings/viewfreebikes.html', {'calendar': mark_safe(calendar),})

@staff_member_required
class ViewBooking(DetailView):
    template_name = 'bookings/bookingdetail.html'
    model = Booking
    context_object_name = 'booking'

@staff_member_required
def view_bookings(request):
    today = Booking.objects.filter(start_date=date.today()).exclude(status='cancl')
    tomorrow = Booking.objects.filter(start_date=date.today()+timedelta(days=1)).exclude(status='cancl')
    day_after_tomorrow = Booking.objects.filter(start_date=date.today()+timedelta(days=2)).exclude(status='cancl')
    return render(request, 'bookings/viewbookings.html', {'today': today,
                                                          'tomorrow': tomorrow,
                                                          'day_after_tomorrow': day_after_tomorrow})
    
def package_display(request):
    packages = Package.objects.filter(active=True)
    return render(request, 'bookings/packagedisplay.html', {'packages': packages})
    
def package_booking(request, slug):
    package = Package.objects.get(slug=slug)
    days = Day.objects.filter(package=package).order_by('order')
    
    if request.method == 'POST':
        form = CustomerPackageBookingForm(request.POST, initial={'package': package.title})
        if form.is_valid():
            data = form.cleaned_data
            # Time variables
            start_date = data['start_date']
            duration = timedelta(days=len(days))
            end_date = start_date + duration - timedelta(days=1)
            date_list = create_date_list(start_date, duration.days)

            # Build bike dictionary
            bikes = {'adult': data['adult_bikes'],'child': data['children'],}
            # Count number of bikes
            number_of_adults = data['adult_bikes']
            number_of_children = data['children']
            # Messages
            biketype_dict = {'adult': 'vuxencykel', 'young': 'ungdomscykel', 'child': 'barncykel',
                    'smallChild': 'småbarncykel'}
            
            bike_list = []
            for biketype, amount in bikes.items():
                if amount is not None and amount > 0:
                    success, list = (BikeAvailable.objects.
                                            get_available_bikes_for_dates(biketype,
                                                                          amount,
                                                                          start_date,
                                                                          end_date,
                                                                          duration))
                    if success:
                        bike_list += list
                    else:
                        return render(request, 'bookings/package.html', {'form': form,
                                                                              'package': package,
                                                                              'days': days,
                                                                              'message': mark_safe('''
                                         Det verkar som att vi inte har tillräckligt många {} lediga<br>
                                         för en eller flera av de önskade dagarna. Ring oss gärna på<br>
                                         0506 - 77 75 50 eller skicka ett mejl till <a href="mailto:info@cafevisthuset.se">
                                         info@cafevisthuset.se</a> så kanske vi kan hjälpa till.
                                         '''.format(biketype_dict[biketype]))})
            # Get or create guest
            guest = Guest.objects.post_get_or_create(data['first_name'],
                                                     data['last_name'],
                                                     data['email'],
                                                     kwargs={'phone_number': data['phone_number'],
                                                             'newsletter': data['newsletter']})
            # Create booking
            booking = Booking.objects.create(guest=guest,
                                        start_date=start_date, 
                                        end_date=end_date,
                                        package=package,
                                        adults=number_of_adults,
                                        children=number_of_children, 
                                        status='unconf',
                                        special_requests=data['other'])
            # Book bikes
            # bike booking not used, but can be used for debugging
            success, bike_booking = booking.setBikeBooking(bike_list, start_date, end_date, duration)

            # Loop over the day to book everythin else included.
            for day in days:
                if day.room:
                    room = Rooms.objects.get(name=day.room.name)
                    # Book rooms, assume always available
                    if data['single_room'] > 0:
                        for num in range(0, data['single_rooms']):
                            RoomsBooking.objects.create(
                                numberOfGuests= 1,
                                from_date=start_date,
                                to_date=end_date,
                                booking=booking,
                                room=room,
                                )
                    if data['shared_room'] > 0:
                        temp = number_of_adults+number_of_children
                        ct = 0
                        for num in range(0, data['shared_room']):
                            ct += 1
                            # Divide the number of guests into shared rooms.
                            # Book each room with the right amount of guests.
                            numguests = temp // data['shared_room']
                            if ct == data['shared_room']:
                                # if last booking, fill up the remainder of guests
                                RoomsBooking.objects.create(
                                    numberOfGuests = temp,
                                    from_date = start_date,
                                    to_date = end_date,
                                    booking=booking,
                                    room = room,
                                )
                            else:
                                # otherwise, fill up number of guests in rooms with divisible number
                                RoomsBooking.objects.create(
                                    numberOfGuests = numguests,
                                    from_date = start_date,
                                    to_date = end_date,
                                    booking = booking,
                                    room = room,
                                    )
                                temp -= numguests   # decrement the number o
                # Lunches are always available
                if day.lunch: 
                    if not day.lunch.type:  # lunch-type == None / choice övrigt
                        LunchBooking.objects.create(
                                type=Lunch.objects.get(slug=day.lunch.slug),
                                day=start_date+timedelta(days=day.order-1),
                                quantity=number_of_adults+number_of_children,
                                booking=booking
                                )
                    else:
                        # Build lunch dictionary
                        lunches ={'veg': data['veg_lunch'], 'fish': data['fish_lunch'], 'meat': data['meat_lunch']}
                        # Book picnic lunches
                        for lunchtype, amount in lunches.items():
                            if amount > 0:
                                LunchBooking.objects.create(
                                    type=Lunch.objects.get(slug=lunchtype), 
                                    day=start_date+timedelta(days=day.order-1),
                                    quantity=amount,
                                    booking=booking)
                            
            # Should not happen
            if not success:
                '''
                TODO:
                # Implement report if something goes wrong and send an email to us. 
                '''
                return render(request, 'failed.html')
        
    else:
        form = CustomerPackageBookingForm(initial={'package': package.title})
    return render(request, 'bookings/package.html', {'package':package,
                                                     'days': days,
                                                     'form': form,})

def confirmation_view(request, pk):    
    booking = Booking.objects.get(booking=pk)
    start_date = booking.start_date
    end_date = booking.end_date
    duration = end_date - start_date
    
    # What to send back to the view        
    c = Context({'booking_number': booking.booking,
        'first_name': booking.guest.first_name,
        'start_date': start_date,
        'duration': int(duration.days),
        'adults': booking.adults,
        'children': booking.children,
        'included_bikes': booking.booked_bike,
        'includes_lunches': booking.booked_lunches,
        'email': booking.guest.email})
    
    # Page texts
    pagename ='bikeconf'
    page = Page.objects.get(code=pagename)
    texts = (PageContent.objects.filter(page__code=pagename, publish=True).exclude(shortname='Cykelbekräftelse')
             .order_by('order'))
    conf = Template(PageContent.objects.get(shortname='Cykelbekräftelse').text)
    ingress = Template(page.ingress)
    headline = Template(page.headline)
    
    # Email stuff
    obj = EmailTexts.objects.get(name='CykelTack')
    
    plain_text = Template(obj.plain_text)
    html_content = Template(obj.html_message)
    
    send_mail(obj.title, plain_text.render(c), 'boka@cafevisthuset.se',
                                [booking.guest.email], ['boka@cafevisthuset.se'],
                                html_message=html_content.render(c))
    
    return render(request, 'bookings/confirmation.html', {'page': page,
                                                          'headline': headline.render(c),
                                                          'ingress': ingress.render(c),
                                                          'confirmation': conf.render(c),
                                                          'texts': texts,})

