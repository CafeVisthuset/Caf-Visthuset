from django.shortcuts import render
from .models import Event
from django.utils.safestring import mark_safe

# Create your views here.

def event(request):
    events = Event.objects.filter(published='True')
    
    return render(request, 'events.html', {'events': events})