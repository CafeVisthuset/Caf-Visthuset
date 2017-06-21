'''
Created on 9 nov. 2016

@author: Adrian
'''
from django import forms
from .models import Booking, Lunch
from database.models import BikeExtra, Bike, LunchBooking, BikesBooking,\
    BikeAvailable, Package, Guest
from .choices import Action_Choices, YEARS, MONTHS
from django.forms.formsets import BaseFormSet
from django.forms.widgets import SelectDateWidget, Select
from datetime import timedelta, date, datetime
from database.helperfunctions import date_list_in_bike_list, create_date_list
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
        fields = ['number', 'bikeKeyNo', 'size', 'extra']
        
class BikeExtraForm(forms.ModelForm):
    class Meta:
        model = BikeExtra
        fields = ['name', 'number']

class BikeBookingForm(forms.ModelForm):
    '''
    Booking form for BikeBooking inline in Admin
    
    TODO:
    # Gör det möjligt (eventuellt genom ett nytt formulär) att boka en grupp cyklar.
    # Lägg in has_changed så att bokning uppdateras utefter om formuläret uppdateras,
        t.ex om man byter cykel i admin.
    '''
    bike = forms.ModelChoiceField(queryset=Bike.objects.all(), required=False)
    from_date = forms.DateField(widget=SelectDateWidget(years=YEARS, months=MONTHS))
    
    class Meta:
        model = BikesBooking
        fields = ['bike', 'out', 'returned', 'from_date','duration', 'subtotal']
        
    def clean(self):
        cleaned_data = super(BikeBookingForm, self).clean()
        
        from_date = cleaned_data.get('from_date')
        duration = cleaned_data.get('duration')
        bike = cleaned_data.get('bike')
        booking = cleaned_data.get('booking')
        # Create list of dates
        date_list = create_date_list(from_date, duration.days)
        
        # Create list of available dates for bike
        bk = BikeAvailable.objects.filter(bike=bike, available=True)
        bike_dates = [bike.available_date for bike in bk]
                 
        if cleaned_data['DELETE']:
            # Can only remove bikes that are not booked
            [BikeAvailable.objects.unbook_bike(
                bike=bike, date=date) for date in date_list]
        
        # Extra validation to make sure that an item that is already included in
        # a booking does not raise a ValidationError when booking is changed
     
        # Find all booked dates for the bike between the start and end date.
        all_booked_bikes = BikeAvailable.objects.filter(bike=bike, available=False, 
                                            available_date__gte=from_date,
                                            available_date__lte=from_date+duration)

        booked_by_me = True
        for bike in all_booked_bikes:
            if bike.bookings != cleaned_data.get('id'):
                booked_by_me = False

        # Validation to make sure that the bike is not already booked
        if not date_list_in_bike_list(date_list, bike_dates) and booked_by_me == False:
                raise forms.ValidationError(
                    'Denna cykel är inte tillgänglig ett eller flera av dessa datum'
                )
"""
TODO:
Gör formsets för barn så att det går att välja ålder på varje enskilt barn.
Cyklarna ska därmed bestämmas utefter det.
"""
class ChildBikeBookingForm(forms.Form):
    age = forms.IntegerField(widget=forms.Select(attrs={'class': 'form-control'},
                                                 choices=[number for number in range(6, 16)]),
                             required=False, label='Ålder')
    
class ChildBikeFormset(BaseFormSet):
    def clean(self):
        for form in self.forms:
            if form.cleaned_data['age'] < 0:
                raise forms.ValidationError('Felaktigt värde på åldern!')
            elif form.cleaned_data['age'] > 15:
                raise forms.ValidationError('Personer över 15 räknas som vuxna.')
            elif form.cleaned_data['age'] == None:
                pass
                
        
class AdminLunchBookingForm(forms.ModelForm):
    type = forms.ModelChoiceField(queryset=Lunch.objects.all())
    
    class Meta:
        model = LunchBooking
        fields = ['type', 'quantity', 'day', 'subtotal']
        help_texts = {'quantity': 'Hur många av den givna lunchen?'}
        label = {'quantity': 'kvantitet', 'subtotal': 'delsumma',
                 'type': 'Lunchtyp'}

class CustomerLunchBookingForm(forms.Form):
    type = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'},
                                                 choices=Lunch.objects.filter(type='picnic')),
                             label='Val')
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
    from_date = forms.DateField(widget=SelectDateWidget(years=YEARS,
                                        empty_label='Välj...'))
    to_date = forms.DateField(widget=SelectDateWidget(years=YEARS,
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
class CustomerBikeBookingForm(forms.Form):
    '''
    Form for booking bike by customer.
    '''
    # Dates and time
    start_date = forms.DateField(label='Startdag', required=True,
                                 initial=date.today(),
                                 widget=forms.SelectDateWidget(
                                     years=[date.today().year],
                                     attrs={'class':'form-control',
                                            'style':'width:32.5%; display:inline-block;'}))
    duration = forms.DurationField(label='Antal dagar', initial=1, required=True,
                                   widget=Select(attrs={'class': 'form-control'},
                                                 choices=Day_Choices))
    
    # Bikes and extras
    adult_bikes = forms.IntegerField(label='Antal vuxencyklar',
        initial=2, widget=forms.Select(attrs={'class':'form-control'},
        choices=[(number, '%s' % (number)) for number in range(0,21)]))
    young_bikes = forms.IntegerField(label='Antal ungdomscyklar(12-16 år)',
        initial=0, widget=forms.Select(attrs={'class':'form-control'},
        choices=[(number, '%s' % (number)) for number in range(0,4)]))
    child_bikes = forms.IntegerField(label='Antal barncyklar(9-12 år)',
        initial=0, widget=forms.Select(attrs={'class':'form-control'},
        choices=[(number, '%s' % (number)) for number in range(0,4)]))
    small_child_bikes = forms.IntegerField(label='Antal småbarncyklar (6-9 år)',
        initial=0, widget=forms.Select(attrs={'class':'form-control'},
        choices=[(number, '%s' % (number)) for number in range(0,4)]))
    #number_extras = forms.MultipleChoiceField(
    #    choices=BikeExtra.objects.all())
    
    # Lunches
    veg_lunch = forms.IntegerField(initial=0, validators=[positive_integer],
                                   label='Vegetarisk', 
                                   widget=forms.NumberInput(attrs={'class':'form-control'}))
    meat_lunch = forms.IntegerField(initial=0, validators=[positive_integer],
                                    label='Kallskuret',
                                    widget=forms.NumberInput(attrs={'class':'form-control'}))
    fish_lunch = forms.IntegerField(initial=0, validators=[positive_integer],
                                    label='Fisk',
                                    widget=forms.NumberInput(attrs={'class':'form-control'}))
    
    # Guest info
    first_name = forms.CharField(max_length=25, label='Förnamn', required=True,
                                 widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(label='Efternamn', max_length=25,
                                widget=forms.TextInput(attrs={'class':'form-control'}))
    phone_number = forms.CharField(max_length=25, required=False, label='Telefon',
                                   widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label='Epost', widget=forms.EmailInput(attrs={'class':'form-control'}))
    newsletter = forms.BooleanField(
        label='Nyhetsbrev',
        initial = True,
        help_text= 'Vill du ha nyheter och erbjudanden från oss?')
    
    # Extra message
    other = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}), max_length=200,
                            required=False, label='Övrig informatio, t.ex. allergier')
    
class CustomerPackageBookingForm(forms.Form):
    '''
    Form for booking packages by customer.
    '''   
    # Dates and time
    package = forms.CharField(label = 'Paket', required = False,
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                           'disabled': None}))
    start_date = forms.DateField(label='Startdag', required=True,
                                 initial=date.today(),
                                 widget=forms.SelectDateWidget(
                                     years=[date.today().year],
                                     attrs={'class':'form-control',
                                            'style':'width:32.5%; display:inline-block;'}))
     # Bikes and extras
    adult_bikes = forms.IntegerField(label='Antal vuxna',
        initial=2, widget=forms.Select(attrs={'class':'form-control'},
        choices=[(number, '%s' % (number)) for number in range(0,21)]))
    children = forms.IntegerField(label = 'Antal barn (under 12 år)',
        initial=0, widget=forms.Select(attrs={'class': 'form-control'},
        choices=[(number, '%s' %(number)) for number in range(0,6)]))
    
    # Rooms
    single_room = forms.IntegerField(widget=forms.Select(attrs={'class':'form-control'},
        choices=[(number, '%s' % (number)) for number in range(0,6)]),
                                     label='Antal enkelrum')
    shared_room = forms.IntegerField(widget=forms.Select(attrs={'class':'form-control'},
        choices=[(number, '%s' % (number)) for number in range(0,5)]),
                                      label='Antal flerbäddsrum')
    
    # Lunches
    veg_lunch = forms.IntegerField(initial=0, label='Vegetarisk', 
                                widget=forms.Select(attrs={'class':'form-control'},
                                choices=[(number, '%s' % (number)) for number in range(0,11)]))
    meat_lunch = forms.IntegerField(initial=0, label='Kallskuret',
                                    widget=forms.Select(attrs={'class':'form-control'},
        choices=[(number, '%s' % (number)) for number in range(0,11)]))
    fish_lunch = forms.IntegerField(initial=0, label='Fisk',
                                    widget=forms.Select(attrs={'class':'form-control'},
        choices=[(number, '%s' % (number)) for number in range(0,11)]))
    
    # Guest info
    first_name = forms.CharField(max_length=25, label='Förnamn', required=True,
                                 widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(label='Efternamn', max_length=25,
                                widget=forms.TextInput(attrs={'class':'form-control'}))
    phone_number = forms.CharField(max_length=25, required=False, label='Telefon',
                                   widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label='Epost', widget=forms.EmailInput(attrs={'class':'form-control'}))
    newsletter = forms.BooleanField(
        label='Nyhetsbrev',
        initial = True,
        help_text= 'Vill du ha nyheter och erbjudanden från oss?')
    
    # Extra message
    other = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}), max_length=200,
                            required=False, label='Övrig informatio, t.ex. allergier eller hur ni vill dela upp er i rummen.')
    
class AdminGuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        exclude = ['password1', 'password2']
        labels = {
            'first_name': 'Förnamn',
            'last_name' : 'Efternamn',
            'email' : 'epost',
            'phone_number': 'Telefonnummer',
            'newsletter': 'Nyhetsbrev'
            }