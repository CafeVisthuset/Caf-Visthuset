from django.contrib import admin
from .models import Dagskassa
from Economy.models import Employee, WorkingHours, Tasks, Event
from django.forms.models import modelformset_factory
from Economy.forms import WorkHoursForm


@admin.register(Dagskassa)    
class CashierAdmin(admin.ModelAdmin):
    order = 'date'
    fieldsets = [
        (None,      {'fields' : [ 'date']}),
        ('Kontant/Kort', {'fields' : ['cash', 'card']}),
        ('Specificerad försäljning', {'fields': ['cafeSales', 'iceCreamSales',
                                      'foodShopSales', 'bikeSales', 'booksSales',
                                      'other12Sales', 'other25Sales']}),
        ('Signering',                 {'fields': ['signature', 'comment']}),
        ]
    list_display = (
        'date','cafeSales', 'iceCreamSales', 'foodShopSales', 
        'bikeSales', 'booksSales', 'other12Sales', 'other25Sales', 'signature',
        'comment')
    list_filter = ['date', 'signature']
    search_fields = ['date', 'signature']
        
@admin.register(WorkingHours)
class WorkingHoursAdmin(admin.ModelAdmin):
    form = WorkHoursForm
    fieldsets = [
        (None,      {'fields':['employee']}),
        ('Datum',   {'fields':['date', 'startTime', 'endTime']}),
        ]
    list_display = ['employee', 'date', 'startTime', 'endTime', 'added']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_and_time']
    
@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at', 'performed', 'responsible', 'event']