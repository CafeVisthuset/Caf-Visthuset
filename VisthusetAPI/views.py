from django.shortcuts import render

from docs.models import Page, PageContent
from events.models import Event
from django.views import generic
from django.http.response import HttpResponse

# Create your views here.
def IndexView(request):
    events = Event.objects.filter(published='True').order_by('start_date')
    
    return render(request, 'visthuset_base.html', {'events': events})

class APIIndexView(generic.TemplateView):
    template_name = 'APIindex.html'
    
def meny_view(request):
    pagename = 'meny'
    page = Page.objects.get(name=pagename)
    texts = PageContent.objects.filter(page__name = pagename, publish=True).order_by('order')
    return render(request, 'Visthuset/meny.html', {'page': page, 'texts':texts})

class UthyrningView(generic.TemplateView):
    template_name = 'Visthuset/uthyrning.html' 

class CalendarView(generic.TemplateView):
    template_name = 'Visthuset/calendar.html'
    
class ContactView(generic.TemplateView):
    template_name = 'Visthuset/contact.html'

def contact_view(request):
    pagename = 'contact'
    page = Page.objects.get(name=pagename)
    texts = PageContent.objects.filter(page__name = pagename, publish=True).order_by('order')
    return render(request, 'Visthuset/contact.html', {'page': page, 'texts':texts})

class AboutView(generic.TemplateView):
    template_name = 'Visthuset/about.html'
    
def about_view(request):
    pagename = 'about'
    page = Page.objects.get(name=pagename)
    texts = PageContent.objects.filter(page__name = pagename, publish=True).order_by('order')
    return render(request, 'Visthuset/about.html', {'page':page, 'texts':texts})