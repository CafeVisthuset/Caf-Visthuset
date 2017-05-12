'''
Created on 25 dec. 2016

@author: Adrian

TODO:
# Write update and delete functions for all serializers

'''
from rest_framework import serializers
from database.models import Booking, BikesBooking, Guest, Discount_codes,\
    BikeExtraBooking, BikeExtra
from django.contrib.auth.models import User
from database.choices import Day_Choices
from database.validators import positive_integer
from datetime import timedelta, date
from database.helperfunctions import choicegen
        
class GuestUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=25, required=False)
    phone_number = serializers.CharField(max_length=25, required=False) # temporary debugfield
    class Meta:
        model = Guest
        fields = ['first_name', 'last_name', 'email', 'phone_number',
                  'newsletter']
        
        def create(self, validated_data):
            try:
                user = Guest.objects.get(username=validated_data['email'])
            except:
                user = None
            
            if not user:
                validated_data['password'] = User.objects.make_random_password()
                validated_data['username'] = validated_data['email']
                return Guest.objects.create(**validated_data)
            else:
                return user


class BikeBookingSerializer(serializers.Serializer):
    # Dates and time
    start_date = serializers.DateField(required=True,
                                       label = 'Startdatum',
                                       help_text = 'Vilket datum vill du starta?')
    duration = serializers.ChoiceField(required=True,
                                       choices= Day_Choices,
                                       label='Antal dagar',
                                       help_text='Hur många dagar vill du hyra cykel?')
    
    # Bikes and extras
    adult_bikes = serializers.ChoiceField(choices=choicegen(0, 10),
                                          label = 'Antal Vuxna',
                                          help_text = 'Hur många vuxencyklar vill du hyra?'
                                          )
    young_bikes = serializers.ChoiceField(choices=choicegen(0, 5),
                                          label= 'Antal ungdom (12-16 år)')
    child_bikes = serializers.ChoiceField(choices=choicegen(0,5),
                                          label='Antal barn (9-12 år)')
    small_child_bikes = serializers.ChoiceField(choices=choicegen(0,5),
                                                label='Antal barn (7-9 år)')
    extras = serializers.MultipleChoiceField(choices=BikeExtra.objects.all(),
                                             label='Cykeltillbehör')
    
    # Lunches
    vegetarian_lunches = serializers.IntegerField(required=False,
                                                  validators=[positive_integer],
                                                  label='Lunch - Vegetarisk')
    meat_lunches = serializers.IntegerField(required=False,
                                            validators=[positive_integer],
                                            label='Lunch - Kallskuret')
    fish_lunches = serializers.IntegerField(required=False,
                                            validators=[positive_integer],
                                            label='Lunch - Vätternröding')
    
    # Guest info
    first_name = serializers.CharField(max_length=25,
                                       label='Förnamn')
    last_name = serializers.CharField(max_length=25,
                                      label='Efternamn')
    phone_number = serializers.CharField(max_length=25,
                                         required=False,
                                         label='Telefonnummer')
    email = serializers.EmailField(label='Epost')
    newsletter = serializers.BooleanField(
        default=True,
        label='Nyhetsbrev',
        help_text= 'Vill du ha nyheter och erbjudanden från oss?'
        )
    
    # Extra message
    other = serializers.CharField(required=False,
                                  max_length=200,
                                  label='Övrig information/önskemål',
                                  style={'base_template': 'textarea.html', 'rows': 10,
                                         'placeholder': 'Övrig info du vill ge oss t ex allergier ...'})
