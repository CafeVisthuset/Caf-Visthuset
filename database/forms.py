'''
Created on 9 nov. 2016

@author: Adrian
'''
from django import forms
from .models import Booking, Lunch
from database.models import BikeExtra, Bike, LunchBooking, BikesBooking,\
    BikeAvailable
from .choices import Lunch_Choices, Action_Choices, YEARS, MONTHS
from django.forms.formsets import BaseFormSet
from django.forms.widgets import SelectDateWidget
from datetime import timedelta, date
from database.helperfunctions import date_list_in_bike_list
from database.validators import positive_integer
from database.choices import Day_Choices


'''
TODO:
* Lägg in en kalender där det går att bläddra i bokningar
* 
'''
class BikesForm(forms.ModelForm):
    
    class Meta:
        model = Bike
        fields = ['number', 'bikeKeyNo', 'wheelsize', 'attribute', 'extra']
        
class BikeExtraForm(forms.ModelForm):
    class Meta:
        model = BikeExtra
        fields = ['name', 'number']

class BikeBookingForm(forms.ModelForm):
    '''
    Booking form for BikeBooking inline in Admin
    
    TODO:
    # Lägg till en funktion så att man inte behöver specificera vilken cykel man väljer 
            för ett datum.
    # Gör det möjligt (eventuellt genom ett nytt formulär) att boka en grupp cyklar.
    # Lägg in has_changed så att bokning uppdateras utefter om formuläret uppdateras,
        t.ex om man byter cykel i admin.
    '''
    bike = forms.ModelChoiceField(queryset=Bike.objects.all(), required=False)
    from_date = forms.DateField(widget=SelectDateWidget(years=YEARS, months=MONTHS))
    to_date = forms.DateField(widget=SelectDateWidget(years=YEARS, months=MONTHS))
    
    class Meta:
        model = BikesBooking
        fields = ['bike', 'full_days', 'from_date', 'to_date', 'subtotal']
        readonly_fields = ['subtotal']
        
    def clean(self):
        cleaned_data = super(BikeBookingForm, self).clean()
        
        from_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')
        bike = cleaned_data.get('bike')
        booking = cleaned_data.get('booking')
        
        # Create list of dates
        numdays = to_date.day - from_date.day
        date_list = [(from_date + timedelta(days=x)) for x in range(0,numdays + 1)]
        
        # Create list of available bikes
        bk = BikeAvailable.objects.filter(bike=bike, available=True)
        bike_dates = [bike.available_date for bike in bk]
        
        # Validation to make sure that the start date is before the end date        
        if from_date > to_date:
            raise forms.ValidationError(
                'Startdatumet får inte vara före slutdatumet')
            
        if cleaned_data['DELETE']:
            # Can only remove bikes that are not booked
            [BikeAvailable.objects.unbook_bike(
                bike=bike, date=date) for date in date_list]
        
        # Extra validation to make sure that an item that is already included in
        # a booking does not raise a ValidationError when booking is changed
        
        # Find all booked dated for the bike.
        bk_query = BikeAvailable.objects.filter(bike=bike, available=False)
        
        # Put them in a list
        all_bikes = [bike.bookings.booking for bike in bk_query
                     if bike.available_date in date_list]
        
        booked_by_me = True
        for bike in all_bikes:
            if bike.booking != booking.booking:
                booked_by_me = False

        # Validation to make sure that the bike is not already booked
        if not date_list_in_bike_list(date_list, bike_dates) and booked_by_me == False:
                raise forms.ValidationError(
                    'Denna cykel är inte tillgänglig ett eller flera av dessa datum'
                )
            
            
class LunchBookingForm(forms.ModelForm):
    type = forms.ModelChoiceField(queryset=Lunch.objects.all())
    class Meta:
        model = LunchBooking
        fields = ['type', 'quantity', 'day', 'subtotal']
        help_texts = {'quantity': 'Hur många av den givna lunchen?'}
        label = {'quantity': 'kvantitet', 'subtotal': 'delsumma',
                 'type': 'Lunchtyp'}
        
###############################################################################
'''
Create forms for creating new available bikes

TODO:
# Se till att felet som visas om datumen inte stämmer överens visas i HTML-fältet.
'''
  


class CreateAvailableBikeForm(forms.Form): 
    action = forms.ChoiceField(choices=Action_Choices, required=False)
    bike = forms.ModelChoiceField(queryset=Bike.objects.all(), label='Välj cykel...',
                                  required=False)
    from_date = forms.DateField(widget=SelectDateWidget(years=YEARS, months=MONTHS,
                                        empty_label='Välj...'))
    to_date = forms.DateField(widget=SelectDateWidget(years=YEARS, months=MONTHS,
                                        empty_label='Välj...'))
    

class BaseCreateAvailableBikeFormset(BaseFormSet):
    def clean(self):
        '''
        Cleaning
        '''
        #cleaned_data = super(BikeBookingForm, self).clean()
        #for form in self.forms:
        #    from_date = cleaned_data.get('from_date')
        #    to_date = cleaned_data.get('to_date')
        
        #    if from_date > to_date:
        #        raise forms.ValidationError(
        #            'Startdatumet får inte vara före slutdatumet')
                
###############################################################################
class BookingForm(forms.Form):
    # Dates and time
    start_date = forms.DateField(required=True,
                                 initial=date.today(),
                                 widget=forms.SelectDateWidget)
    duration = forms.ChoiceField(choices=Day_Choices, required=True)
    
    # Bikes and extras
    number_adult_bikes = forms.ChoiceField(
        initial=2,
        choices=[(number, '%s' % (number)) for number in range(0,11)])
    number_child_bikes = forms.ChoiceField(
        choices=[(number, '%s' % (number)) for number in range(0,4)])
    #number_extras = forms.MultipleChoiceField(
    #    choices=BikeExtra.objects.all())
    
    # Lunches
    number_veg_lunches = forms.IntegerField(validators=[positive_integer])
    number_meat_lunches = forms.IntegerField(validators=[positive_integer])
    number_fish_lunches = forms.IntegerField(validators=[positive_integer])
    
    # Guest info
    first_name = forms.CharField(max_length=25)
    last_name = forms.CharField(max_length=25)
    phone_number = forms.CharField(max_length=25, required=False)
    email = forms.EmailField()
    newsletter = forms.BooleanField(
        initial = True,
        help_text= 'Vill du ha nyheter och erbjudanden från oss?')
    
    # Extra message
    other = forms.CharField(widget=forms.Textarea, max_length=200, required=False)