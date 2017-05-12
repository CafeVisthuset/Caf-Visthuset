from Economy.forms import CashForm, WorkHoursForm
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from Economy.models import WorkingHours, Dagskassa
from django.views.generic.edit import CreateView
from django.forms.models import modelformset_factory
from django.views.generic.detail import DetailView
from datetime import datetime
from rest_framework import viewsets
from django.contrib.auth.models import User
from Economy.serializers import UserSerializer
from django.contrib.auth.decorators import login_required
from django.urls.base import reverse

"""
    TODO:
    * Create validation routine for this form
        # comment should not be validated
        # All fields cannot be 0
        # The sum of card and cash must agree with sum of sales
    * Make sure no duplicates of the same form can be made.
    * Style the view
"""

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
def index(request):
    return HttpResponse('här är ekonomisidan')

def ResultsView(request):
    return render(request, 'economy/results.html')

#@login_required()
def CashierView(request):
    if request.method == 'POST':
        form = CashForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/economy/results/')
    else:
        form = CashForm()
    return render(request, 'economy/base_form.html', {'form': form})

#@login_required()
class genCashierView(CreateView):
    template_name ='economy/base_form.html'
    form_class = CashForm
    context_object_name = 'CashCount'
    
    class Meta:
        model = Dagskassa
        fields = ['date']
        
    def form_valid(self, form):
        return super(genCashierView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse('/economy/results/')
        
# Formset for calculating hours worked by staff
@login_required()
class ManageWorkHours(DetailView):
    queryset = WorkingHours.objects.all()[:5]
    class Meta:
        verbose_name = ''
        
data = {
    'form-TOTAL_FORMS': '5',
    'form-INITIAL_FORMS': '0',
    'form-MAX_NUM_FORMS': '10',
}
def working_hours(self, date, starttime, endtime):
    starting = datetime.combine(date, starttime)
    ending = datetime.combine(date, endtime)
    hours = ending - starting
    return hours

@login_required    
def manage_hours_worked(request):
    hoursWorkedFormset = modelformset_factory(WorkingHours, form=WorkHoursForm, fields = (
        'employee', 'date', 'startTime', 'endTime'), validate_min=1)
    if request.method == 'POST':                   
        formset = hoursWorkedFormset(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()               
            return HttpResponse('Du har nu lagt in arbetstimmarna')
    else: 
        formset = hoursWorkedFormset(data)  
    return render(request, 'economy/hours_worked_form.html', {'formset': formset})
