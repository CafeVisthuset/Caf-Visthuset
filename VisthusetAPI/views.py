from django.shortcuts import render
from django.views import generic
from django.http.response import HttpResponse

# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'Visthuset/index.html'

class APIIndexView(generic.TemplateView):
    template_name = 'APIindex.html'
    
class MenuView(generic.TemplateView):
    template_name = 'Visthuset/menu.html'
    
class CalendarView(generic.TemplateView):
    template_name = 'Visthuset/calendar.html'
    
class EventsView(generic.TemplateView):
    template_name = 'Visthuset/events.html'
    
class ContactView(generic.TemplateView):
    template_name = 'Visthuset/contact.html'
    
class AboutView(generic.TemplateView):
    template_name = 'Visthuset/about.html'