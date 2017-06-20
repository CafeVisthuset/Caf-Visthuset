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