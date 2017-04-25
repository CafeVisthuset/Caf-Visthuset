from django.shortcuts import render

from events.models import Event
from django.views import generic
from django.http.response import HttpResponse

# Create your views here.
def IndexView(request):
    events = Event.objects.filter(published='True')
    
    return render(request, 'visthuset_base.html', {'events': events})

class APIIndexView(generic.TemplateView):
    template_name = 'APIindex.html'
    
class MenuView(generic.TemplateView):
    template_name = 'Visthuset/menu.html'
    
class CalendarView(generic.TemplateView):
    template_name = 'Visthuset/calendar.html'
    
class ContactView(generic.TemplateView):
    template_name = 'Visthuset/contact.html'
    
class AboutView(generic.TemplateView):
    template_name = 'Visthuset/about.html'