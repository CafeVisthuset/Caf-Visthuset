from django.shortcuts import render
from .models import Event
from django.utils.safestring import mark_safe

# Create your views here.

def event(request):
    events = Event.objects.filter(published='True').order_by('start_date')
    
    return render(request, 'events.html', {'events': events})