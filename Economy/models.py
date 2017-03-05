from django.db import models
from datetime import date, datetime
from django.contrib.auth.models import User
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
'''
TODO:
* Gör det möjligt att räkna ut lön, skatt och antal arbetade timmar för varje anställd
    - Ge digitalt lönebesked
* Gör formulär för admin att kunna lägga in antalet timmar de anställda jobbat
    - Uppdaterar automatiskt hours_worked

'''
class StaffManager(models.Manager):
    
    def get_queryset(self):
        return super(StaffManager, self).get_queryset().filter(
            Q(is_staff=True) | Q(is_superuser=True))
        
class Staff(User):
    objects = StaffManager()
    class Meta:
        proxy = True
        verbose_name = 'anställd'
        verbose_name_plural = 'anställda'

class WorkingSpecs(models.Model):
    person_number = models.IntegerField(null= True, verbose_name= 'Personnummer')
    wage = models.DecimalField(verbose_name= 'Lön',
        max_digits=6, decimal_places=2, null= True, blank=True)
    
    hours_worked = models.DecimalField(verbose_name='arbetade timmar',
        max_digits=6, decimal_places=2, default = 0)
    
    tax = models.DecimalField(max_digits=4, decimal_places=2, default=33.0,
                              help_text='Preliminärskatt att dra från lönen',
                              verbose_name='preliminärskatt')
    
    drawTax = models.BooleanField(default=True, verbose_name='Dra preliminärskatt',
                                  help_text='skall preliminärskatt dras från lönen?')
    
    ArbAvg = models.DecimalField(max_digits=3, decimal_places=2, default=0.25)
    
    phone_number = models.CharField(max_length=24, blank=True, null=True)
    
    
    class Meta:
        abstract = True
        
class Employee(Staff, WorkingSpecs):

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)
    
    def get_full_name(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)
    
    def update_hours_worked(self, hours):
        self.hours_worked += hours
        return self.hours_worked
    
    
    class Meta:
        verbose_name = 'anställd'
        verbose_name_plural = 'anställda'
   
class WorkingHours(models.Model):
    employee = models.ForeignKey(
        Employee,
        null=True,
        verbose_name='anställd'
        )
    date = models.DateField(verbose_name='datum')
    startTime = models.TimeField(verbose_name='starttid')
    endTime = models.TimeField(verbose_name='sluttid')
    added = models.DateTimeField(default=datetime.now, verbose_name= 'Tillagd')
    
    class Meta:
        verbose_name='arbetstimme'
        verbose_name_plural='arbetstimmar'
        unique_together = ['employee', 'date', 'added']

# Modell för att lägga in dagskassor
class Dagskassa(models.Model):
    date = models.DateField(default= date.today, verbose_name='datum')
    
    cash = models.DecimalField(
        max_digits = 7, decimal_places = 2, default=0, verbose_name='kontanter')
    
    card = models.DecimalField(
        max_digits = 7, decimal_places = 2, default=0, verbose_name='kort')
    
    cafeSales = models.DecimalField(
        max_digits = 7, decimal_places = 2, default=0, verbose_name='café')
    
    iceCreamSales = models.DecimalField(
        max_digits = 7, decimal_places = 2, default=0, verbose_name='glass')
    
    foodShopSales = models.DecimalField(
        max_digits = 7, decimal_places = 2, default=0, verbose_name='gårdsbutik')
    
    bikeSales = models.DecimalField(
        max_digits = 7, decimal_places = 2, default=0, verbose_name='cyklar')
    
    booksSales = models.DecimalField(
        max_digits = 7, decimal_places = 2, default=0, verbose_name='böcker')
    
    other12Sales = models.DecimalField(
        max_digits = 7, decimal_places = 2, default=0, verbose_name='övrigt 12%')
    
    other25Sales = models.DecimalField(
        max_digits = 7, decimal_places = 2, default=0, verbose_name='övrigt 25%')
    
    signature = models.ForeignKey(Employee,
        on_delete=models.CASCADE,
        verbose_name='Signatur'
        )
    
    comment = models.CharField(max_length = 150, null=True, verbose_name='kommentar')
    
    # Check at which times the daycount has been updated
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'dagskassa'
        verbose_name_plural = 'dagskassor'
        ordering = ('date', )
        unique_together = ['date', 'cash', 'card', 'signature']
        

class Price(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='pris exkl. moms')
    
    # Generic foreign key
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    
'''
Event model class for creating events and show in a calendar on the admin index
page. 

TODO:
# Create autocreation for events, e.g., from cleaning

'''
    
class Event(models.Model):
    title = models.CharField(max_length=24)
    short_description = models.TextField(max_length=100)
    
    # Date of the event
    date_and_time = models.DateTimeField()
    
    class Meta:
        verbose_name = 'Händelse'
        verbose_name_plural = 'Händelser'
    
    def __str__(self):
        return self.title
    
class Tasks(models.Model):
    # Basic describtion
    title = models.CharField(max_length = 25)
    description = models.TextField(max_length = 255)
    
    # Times and dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Has it been done?
    responsible = models.ForeignKey(
        Employee,
        null = True,
        blank = True,
        on_delete=models.CASCADE,
        related_name = 'responsible'
        )
    common_task = models.BooleanField(default=True, help_text=
                                      'Är den här uppgiften gemensam för alla?')
    performed = models.BooleanField(default=False)
    
    # Event associated with the task
    event = models.ForeignKey(
        Event,
        on_delete = models.CASCADE,
        related_name = 'tasks',
        
        )
    
    class Meta:
        verbose_name = 'Uppgift'
        verbose_name_plural = 'Uppgifter'
    
    def __str__(self):
        return self.title