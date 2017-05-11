from django.db import models
from datetime import date, datetime
from Economy.models import Employee
from cleaning.choices import Weekday_Choices
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db.models.base import Model

"""
TODO:
* Lägg in verbose_name för alla fält
* Lägg in beställningsrutiner och telefonnumer, eventuellt som en flatpage
* Lägg in schema för personalen
"""
class Supplier(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    contact = models.CharField(max_length=30, verbose_name='kontaktperson')
    order_day = models.CharField(max_length=15, choices=Weekday_Choices,
            help_text='Veckodag för beställning')

    description = models.TextField(max_length=200, blank=True)
    goods = models.TextField(max_length=100, blank=True)

    other = models.TextField(max_length=200, blank=True)

    class Meta:
        verbose_name='leverantör'
        verbose_name_plural='leverantörer'

    def __str__(self):
        return self.name

class Routine(models.Model):
    name = models.SlugField(max_length=25)
    purpose = models.TextField(max_length=150)
    description = models.TextField(max_length=500)
    monitoring = models.TextField(max_length=500)
    anomaly_measure = models.TextField(max_length=150)
    anomaly_correction = models.TextField(max_length=150)
    
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    
    class Meta:
        verbose_name = 'rutin'
        verbose_name_plural = 'rutiner'
        ordering = ['name', '-updated']
    
FROM = [
    ('physical', 'Fysisk fara'),
    ('chemical', 'Kemisk fara'),
    ('microbio', 'Mikrobiologisk fara'),
    ('allergic', 'Allergen fara'),
    ]

HOW = [
    ('occurence', 'Förekomst'),
    ('application', 'Tillförsel'),
    ('growth', 'Tillväxt'),
    ('survival', 'Överlevnad'),
    ]
class Hazard(models.Model):
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    content_object = GenericForeignKey()
    type = models.CharField(max_length=15, choices=FROM)
    how = models.CharField(max_length=15)
    description = models.TextField(max_length=500)
    routine = models.ForeignKey(
        Routine,
        related_name='routine',
        on_delete=models.PROTECT,
        blank=True
        )
    routine_sufficient = models.BooleanField(default = True)
    analysis = models.TextField(max_length=1000, verbose_name='faroanalys')
    
RECCURRENCE = [
    ('yearly', 'Årligen'),
    ('monthly', 'Månadsvis'),
    ('weekly', 'Veckovis'),
    ('2week', '2 ggr/vecka'),
    ('3week', '3 ggr/vecka'),
    ('daily', 'dagligen'),
    ]

TYPES = [
    ('coldstor', 'Kylförvaring'),
    ('storage', 'Lagring'),
    ('preparation', 'Beredning'),
    ('serving', 'Servering'),
    ]
class ControlPoint(models.Model):
    type = models.CharField(max_length=15, choices=TYPES, blank=False)
    name = models.CharField(max_length=25)
    location = models.CharField(max_length = 255)
    short_description = models.TextField(max_length=255)
    active = models.BooleanField(default=True)
    hazard = GenericRelation(Hazard)
    routine = models.ForeignKey(
        Routine,
        related_name='routine',
        on_delete=models.PROTECT,
        )
    routine_recurr = models.CharField(max_length=15, choices=RECCURRENCE)
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    documentation = GenericForeignKey()
    
    created = models.DateField(auto_now_add=True, verbose_name='Skapad')
    updated = models.DateField(auto_now = True, verbose_name='Uppdaterad')

class ColdStorageManager(models.Manager):
    def get_queryset(self):
        return super(ColdStorageManager, self).get_queryset().filter(
            type='coldstor')
        
    def create(self, **kwargs):
        kwargs.update({'type':'coldstor'})
        return super(StorageManager, self).create(**kwargs)
    
class ColdStorageExtra(models.Model):
    kind = models.CharField(max_length=15, 
                            choices=[('freeze', 'Frys'), ('fridge', 'kyl'), ('cool', 'sval')])
    prescribedMaxTemp = models.IntegerField()
    prescribedMinTemp = models.IntegerField()
    
    class Meta:
        abstract = True
        
class ColdStorage(ControlPoint, ColdStorageExtra):
    objects = ColdStorageManager()
    class Meta:
        proxy=True
        verbose_name='kontrollpunk - Kylförvaring'
        verbose_name_plural = 'kontrollpunkter - Kylförvaring'
        

class StorageManager(models.Manager):
    def get_queryset(self):
        return super(StorageManager, self).get_queryset().filter(
            type = 'storage')
        
    def create(self, **kwargs):
        kwargs.update({'type':'storage'})
        return super(StorageManager, self).create(**kwargs)
    
class Storage(ControlPoint):
    objects = StorageManager()
    class Meta:
        verbose_name='kontrollpunkt - Lagring'
        verbose_name_plural = 'kontrollpunkter - Lagring'
        proxy = True
        
class PreparationManager(models.Manager):
    def get_queryset(self):
        return super(PreparationManager, self).get_queryset().filter(
            type='preparation')
        
    def create(self, **kwargs):
        kwargs.update({'type':'preparation'})
        return super(StorageManager, self).create(**kwargs)
        
class Preparation(ControlPoint):
    objects = PreparationManager()
    class Meta:
        proxy= True
        verbose_name='kontrollpunk - Beredning'
        verbose_name_plural='kontrollpunkter - Beredning'
        ordering = ['-active', '-updated']

class ServingManager(models.Manager):
    def get_queryset(self):
        return super(ServingManager, self).get_queryset().filter(
            type = 'serving')
        
    def create(self, **kwargs):
        kwargs.update({'type':'serving'})
        return super(StorageManager, self).create(**kwargs)
    
class Serving(ControlPoint):
    objects = ServingManager()
    class Meta:
        proxy=True
        verbose_name='kontrollpunkt - Servering'
        verbose_name_plural='kontrollpunkter - Servering'
        
class CriticalControlPointManager(models.Manager):
    def get_queryset(self):
        return super(CriticalControlPointManager, self).get_queryset().filter(
            hazard__routine_sufficient = False) 
    
class CriticalControlPointExtra(models.Model):
    upper_limit = models.CharField(max_length=100)
    lower_limit = models.CharField(max_length=100)
    extra_monitoring = models.TextField(max_length=500)
    
    class Meta:
        abstract = True
        
class CriticalControlPoint(ControlPoint, CriticalControlPointExtra):
    objects = CriticalControlPointManager()
    class Meta:
        proxy = True
        
class Documentation(models.Model):
    control_point = GenericRelation(ControlPoint, many_to_one=True, one_to_many=False)
    anomaly = models.BooleanField(default=False, verbose_name='avvikelse')
    measure = models.CharField(blank=True, max_length=100, verbose_name='åtgärd',
        help_text='Vilken åtgärd har tagits?')
    comment = models.TextField(max_length=255, blank=True, verbose_name='kommentar')
    
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    
    def open_visthuset(self):
        if not self.open:
            self.open = True
            return self.open
        else:
            self.open = False
        return self.open
    
    
class Temperature(Documentation):
    measured = models.IntegerField(verbose_name='Uppmätt temperatur')
    defrosted = models.BooleanField(default=False, verbose_name='Avfrostad')
    
    class Meta:
        verbose_name = 'dokumentera temperatur'
        verbose_name_plural = 'dokumentera temperaturer'

    '''
    TODO:
    # Funktion för att sätta anomaly på denna
    
    '''
class Clean(Documentation):
    clean = models.BooleanField(default=False)

    class Meta:
        app_label = 'dokumentation'
        verbose_name = 'städning'
        verbose_name_plural = 'städning'
        ordering = ['date']
    
    def save(self):
        if not self.clean:
            self.anomaly = True
        self.save()
        

class Delivery(Documentation):
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        null=True,
        )
    smell = models.BooleanField(default=True)
    damaged = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'leverans'
        verbose_name_plural = 'leveranser'
        ordering = ['date']

    def __str__(self):
        return '{}, {}'.format(self.supplier, self.date)

    def save(self):
        if self.damaged or self.expired or not self.smell:
            self.anomaly = True
        self.save()   
    
class FacilityDamage(Documentation):
    repaired = models.BooleanField(default=False)
    localtion = models.TextField(max_length=100)
    description = models.TextField(max_length=500)
    
    class Meta:
        verbose_name = 'fastighetsskada'
        verbose_name_plural = 'fastighetsskador'
        ordering = ['-anomaly', '-date']
    
    def save(self):
        if not self.repaired:
            self.anomaly = True
        self.save()    
        
class Allergen(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=200, blank=True)
    hazard = GenericRelation(Hazard)
    
    class Meta:
        verbose_name = 'allergen'
        verbose_name_plural='allergener'
        
    def __str__(self):
        return self.name

##############################################################################
###                                                                        ###
###                            RECEPIE DATABASE                            ###
###                                                                        ###
##############################################################################

class Ingredience(models.Model):
    name = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=6, decimal_places=2,
                                help_text='Pris/kg eller pris/l')
    package_size = models.CharField(max_length=30, blank=True,
                    help_text='storlek på paket, om standard. Ex. 25 kg säck')
    allergen = models.ManyToManyField(
        Allergen,
        )

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        blank=True
        )

    class Meta:
        verbose_name = 'ingrediens'
        verbose_name_plural = 'ingredienser'

    def __str__(self):
        return self.name

class RecepieIngredience(models.Model):
    ingredience = models.ForeignKey(
        Ingredience,
        on_delete=models.PROTECT,
        )
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    recepie = models.ForeignKey(
        'Recepie',
        on_delete=models.PROTECT,
        blank= True,
        null=True
        )

    def __str__(self):
        return self.ingredience.name

class Recepie(models.Model):
    name = models.CharField(max_length=50)
    pieces = models.IntegerField(help_text='Antal per sats')
    customer_price = models.DecimalField(max_digits=5, decimal_places=2)
    retailer_price = models.DecimalField(max_digits=5, decimal_places=2)
    work_hours = models.DurationField(help_text='Arbetsinsats för en sats')
    oven_time = models.DurationField(help_text='Tid i ugnen')

    description = models.TextField(max_length=1000, help_text='Hur gör man?')

    added = models.TimeField(auto_now_add=True)
    updated = models.TimeField(auto_now=True)

    class Meta:
        verbose_name = 'recept'
        verbose_name_plural = 'recept'
        ordering = ['name']

    def __str__(self):
        return self.name

class Production(models.Model):
    amount = models.PositiveIntegerField(verbose_name='antal satser')
    recepie = models.ForeignKey(
        Recepie,
        on_delete=models.PROTECT,
        related_name='production',
        verbose_name='recept'
        )
    date = models.DateField(default=date.today, verbose_name='datum')
    signature = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name='signature',
        verbose_name='signatur'
        )
    
    class Meta:
        verbose_name = 'produktion'
        verbose_name_plural = 'produktion'
        ordering = ['date']