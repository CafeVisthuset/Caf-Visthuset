'''
Created on 9 nov. 2016

@author: Adrian
'''
from django.forms.models import ModelForm
from django import forms
# Special Choice Fields for models
class ColdStorageChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return"%s, %s"%(obj.type, obj.location)
      
