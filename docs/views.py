from django.shortcuts import render
from django.views import generic
from django.http.response import HttpResponse
from database.models import Employee

# Create your views here.
def index(request):
    return HttpResponse("Welcome to the docs section!")

class IndexView(generic.TemplateView):
    template_name = 'docs/Index.html'
    
class LandingView(generic.TemplateView):
    template_name = 'index.html'
    
def tutor(request):
    damages_list = Employee.objects.all()
    output = ", ".join([damage.first_name for damage in damages_list])
    return HttpResponse(output)