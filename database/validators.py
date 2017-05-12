'''
Created on 26 nov. 2016

@author: Adrian
'''
from datetime import date
from django.core.exceptions import ValidationError

# Booking validators
def validate_booking_date(value):
    if value > date.today:
        raise ValidationError(
            'Bokningsdatumet måste vara för idag'
            )

def validate_preliminary(self):
    if self.preliminary == False:
        raise ValidationError(
            'Detta är ingen preliminärbokning'
            )

def positive_integer(self):
    if self < 0:
        raise ValidationError(
            'Fältet får inte vara mindre än 0'
            )
        