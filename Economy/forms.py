'''
Created on 12 nov. 2016

@author: Adrian
'''
from .models import Dagskassa
from django.forms import ModelForm, Textarea
from django import forms
from Economy.models import WorkingHours
from django.forms.models import BaseModelFormSet

"""
    TODO:
    * Lägg till en snyggare css+js-widget för datumet genom en Form Asset.
    * skriv klart labels
    * skriv klart helper_texts
    * lägg till error_messages
"""
class NameChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s %s" % (obj.first_name, obj.last_name)
    
class CashForm(ModelForm):
    """
    Formulär för att lägga in dagskassor
    """
    class Meta:
        model = Dagskassa
        fields =['date', 'cash', 'card','cafeSales', 'iceCreamSales', 'foodShopSales', 
                 'bikeSales', 'booksSales', 'other12Sales', 'other25Sales', 'signature',
                'comment']
        widgets = {
            'comment': Textarea(attrs={'cols': 50, 'rows' : 10}),
            }
        labels = {
            'date': "Datum:",
            'cash': "Kontanter:",
            'card': "Kort:",
            'comment': "Kommentar",
            }
        help_texts = {
            'date' : "vilket datum gäller dagskassan?",
            'comment' : "Om något inte stämmer kan du lägga till en kommentar här",
            }
        widgets = {
            'comment': Textarea(attrs={'cols': 50, 'rows' : 10}),
            }
        labels = {
            'date': "Datum:",
            'cash': "Kontanter:",
            'card': "Kort:",
            'comment': "Kommentar",
            }
        help_texts = {
            'date' : "vilket datum gäller dagskassan?",
            'comment' : "Om något inte stämmer kan du lägga till en kommentar här",
            }
        error_message = {
            'date' : 'Denna måste fyllas i',
            'signature' : 'denna måste fyllas i',
            }

SpecDateFormat = ['%d/%m-%y', ]
SpecTimeFormat = ['%H.%M', ]

class WorkHoursForm(forms.ModelForm):
    
    class Meta:
        model = WorkingHours
        fields = ('employee', 'date', 'startTime', 'endTime')
        labels ={'employee': 'Namn',
                 'date': 'Datum',
                 'startTime': 'Började:',
                 'endTime': 'Slutade:',
                 } 
        help_texts ={
            'employee': 'vem jobbade arbetspasset?',
            'startTime': 'När började arbetspasset? Ange i format hh.mm, dd/mm',
            'endTime': 'När slutade arbetspasset? Ange i format hh.mm, dd/mm'
            }
        error_messages={
            'required': 'Du måste ange det här fältet!',
            'invalid': 'Ange rätt format!'
            }
        
class BaseWorkHours(BaseModelFormSet):    
    def clean(self):
        '''Checks so that there are no replicate working hours put in'''
        super(WorkHoursForm, self).clean()
        names = []
        dates = []
        startTimes = []
        endTimes = []
        for form in self.forms:
            name = form.cleaned_data('name')
            day = form.cleaned_data('date')
            startTime = form.cleaned_data('startTime')
            endTime = form.cleaned_data('endTime')
            if startTime in startTimes and day in dates and name in names:
                raise forms.ValidationError('Du håller på att lägga in dubbla pass för en anställd\
                samma dag, det är inte tillåtet. Lägg in direkt i databasen om detta ändå är korrekt')
            
            names.append(name)
            dates.append(day)
            startTimes.append(startTime)
            endTimes.append(endTime)
