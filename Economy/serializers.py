'''
Created on 7 dec. 2016

@author: Adrian
'''
# Serializers define the API representation.
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')