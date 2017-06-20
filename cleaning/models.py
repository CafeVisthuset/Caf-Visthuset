from django.db import models
from datetime import date
from Economy.models import Employee
from cleaning.choices import Weekday_Choices
from django.core.exceptions import ObjectDoesNotExist
from .validators import validateTemperatureAnomaly

"""
TODO:
* Lägg in verbose_name för alla fält
* Lägg in beställningsrutiner och telefonnumer, eventuellt som en flatpage
* Lägg in schema för personalen
"""
class Supplier(models.Model):
    name = models.CharField(max_length=50, verbose_name='namn')
    phone = models.CharField(max_length=20, verbose_name='telefon')
    email = models.EmailField(blank=True, verbose_name='Epost')
    contact = models.CharField(max_length=30, verbose_name='kontaktperson')
    order_day = models.CharField(max_length=15, choices=Weekday_Choices,
            help_text='Veckodag för beställning')

    description = models.TextField(max_length=200, blank=True, verbose_name='beskrivning')

    other = models.TextField(max_length=200, blank=True, verbose_name='Övrigt',
                             help_text='Till exempel att tänka på vid beställning')

    class Meta:
        verbose_name='leverantör'
        verbose_name_plural='leverantörer'

    def __str__(self):
        return self.name

class Routine(models.Model):
    name = models.CharField(max_length=25)
    purpose = models.TextField(max_length=150)
    description = models.TextField(max_length=500)
    monitoring = models.TextField(max_length=500)
    anomaly_measure = models.TextField(max_length=150)
    anomaly_correction = models.TextField(max_length=150)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'rutin'
        verbose_name_plural = 'rutiner'
        ordering = ['name', '-updated']
    def __str__(self):
        return self.name
    
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
    name = models.CharField(max_length=25)
    type = models.CharField(max_length=15, choices=FROM)
    how = models.CharField(max_length=15, choices=HOW)
    description = models.TextField(max_length=500)
    analysis = models.TextField(max_length=1000, verbose_name='faroanalys')
    
    class Meta:
        verbose_name = 'Fara'
        verbose_name_plural = 'Faror'
        
    def __str__(self):
        return self.name
    
RECCURRENCE = [
    ('yearly', 'Årligen'),
    ('monthly', 'Månadsvis'),
    ('weekly', 'Veckovis'),
    ('2week', '2 ggr/vecka'),
    ('3week', '3 ggr/vecka'),
    ('daily', 'Dagligen'),
    ('always', 'Vid varje tillfälle')
    ]

class ControlPoint(models.Model):
    name = models.CharField(max_length=25, verbose_name='Namn')
    location = models.CharField(max_length = 255, verbose_name='Plats')
    short_description = models.TextField(max_length=255, verbose_name='Kort beskrivning')
    active = models.BooleanField(default=True, verbose_name='Används den?')
    hazard = models.ManyToManyField(Hazard, verbose_name='Fara')
    
    routine_recurr = models.CharField(max_length=15, choices=RECCURRENCE,
                                      verbose_name='Hur ofta utförs rutinen?')
    routine_sufficient = models.BooleanField(default=True)
    
    created = models.DateTimeField(auto_now_add=True, verbose_name='Skapad')
    updated = models.DateTimeField(auto_now = True, verbose_name='Uppdaterad')
    
    class Meta:
        ordering = ['-active', '-updated']
        
    def __str__(self):
        return self.name
    
class RiskAnalysis(models.Model):
    control_point = models.ForeignKey(
        ControlPoint, 
        on_delete=models.DO_NOTHING,
        verbose_name='kontrollpunkt',
        )
    routine = models.ForeignKey(
        Routine,
        on_delete=models.DO_NOTHING,
        verbose_name='Rutin'
        )
    routine_recurr = models.CharField(max_length=15, choices=RECCURRENCE,
                                      verbose_name='Hur ofta utförs rutinen?')
    routine_sufficient = models.BooleanField(default=True)
    comment = models.TextField(max_length=200, verbose_name='kommentar', blank=True)
    
    class Meta:
        verbose_name='Rutin för kontrollpunkt'
        verbose_name_plural='Rutiner för kontrollpunkter'
    
def auto_increment():
    try:
        storage = ColdStorage.objects.latest('number')
    except ObjectDoesNotExist:
        storage = 0
    return storage.number + 1

class ColdStorage(ControlPoint):
    number = models.PositiveIntegerField()#default=auto_increment)
    kind = models.CharField(max_length=15, 
                            verbose_name='Typ',
                            choices=[('freeze', 'Frys'), ('fridge', 'kyl'), ('cool', 'sval')])
    prescribedMaxTemp = models.IntegerField(verbose_name='Maxtemperatur')
    prescribedMinTemp = models.IntegerField(verbose_name='Minimumtemperatur')
    
    class Meta:
        verbose_name='kontrollpunk - Temperatur'
        verbose_name_plural = 'kontrollpunkter - Temperatur'
        
    def __str__(self):
        return '{}. {}'.format(self.number, self.name)
        
class Storage(ControlPoint):

    class Meta:
        verbose_name='kontrollpunkt - Lagring'
        verbose_name_plural = 'kontrollpunkter - Lagring'
        

class Preparation(ControlPoint):

    class Meta:
        verbose_name='kontrollpunk - Beredning'
        verbose_name_plural='kontrollpunkter - Beredning'

class Serving(ControlPoint):

    class Meta:
        verbose_name='kontrollpunkt - Servering'
        verbose_name_plural='kontrollpunkter - Servering'

class CriticalControlPoint(ControlPoint):
    upper_limit = models.CharField(max_length=100, verbose_name='Övre gräns')
    lower_limit = models.CharField(max_length=100, verbose_name='Nedre gräns')
    extra_monitoring = models.TextField(max_length=500, verbose_name='Extra övervakning')

    class Meta:
        verbose_name='kritisk kontrollpunkt'
        verbose_name_plural='kritiska kontrollpunkter'
   
class Documentation(models.Model):
    date = models.DateField(default=date.today, verbose_name='Datum')
    anomaly = models.BooleanField(default=False, verbose_name='Avvikelse')
    measure = models.CharField(blank=True, max_length=100, verbose_name='Åtgärd',
        help_text='Vilken åtgärd har tagits?')
    
    comment = models.TextField(max_length=255, blank=True, verbose_name='kommentar')
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        
class Temperature(Documentation):
    control_point = models.ForeignKey(
        ColdStorage,
        on_delete=models.PROTECT,
        verbose_name='Kontrollpunkt'
        )
    measured = models.IntegerField(verbose_name='Uppmätt temperatur')
    signature = models.ForeignKey(
        Employee, 
        on_delete=models.PROTECT,
        verbose_name='signatur',
        )
    class Meta:
        verbose_name = 'dokumentera temperatur'
        verbose_name_plural = 'dokumentera temperaturer'
        ordering = ['date']

   
class Clean(Documentation):
    control_point = models.ForeignKey(
        ControlPoint,
        on_delete=models.PROTECT,
        verbose_name='Kontrollpunkt'
        )
    cleaned = models.BooleanField(default=False, verbose_name='Städat?')
    signature = models.ForeignKey(
        Employee, 
        on_delete=models.PROTECT,
        verbose_name='signatur',
        )
    class Meta:
        verbose_name = 'Dokumentera städning'
        verbose_name_plural = 'Dokumentera städning'
        
    def save(self):
        if not self.cleaned:
            self.anomaly = True

        

class Delivery(Documentation):
    supplier = models.ForeignKey(
        Supplier,
        verbose_name='Leverantör',
        on_delete=models.PROTECT,
        null=True,
        )
    smell = models.BooleanField(default=True, verbose_name='Lukt ok?')
    damaged = models.BooleanField(default=False, verbose_name='Förpackning ok?')
    expired = models.BooleanField(default=False, verbose_name='Datum ok?')
    note = models.CharField(max_length=30, verbose_name='Följesedel')
    signature = models.ForeignKey(
        Employee, 
        on_delete=models.PROTECT,
        verbose_name='signatur',
        )
    class Meta:
        verbose_name = 'Dokumentera leverans'
        verbose_name_plural = 'Dokumentera leveranser'
        ordering = ['date']

    def __str__(self):
        return '{}, {}'.format(self.supplier, self.date)


class FacilityDamage(Documentation):
    repaired = models.BooleanField(default=False, verbose_name='Reparerad?')
    location = models.TextField(max_length=100, verbose_name='Plats')
    description = models.TextField(max_length=500, verbose_name='Beskrivning')
    signature = models.ForeignKey(
        Employee, 
        on_delete=models.PROTECT,
        verbose_name='signatur',
        )
    
    class Meta:
        verbose_name = 'Dokumentera fastighetsskada'
        verbose_name_plural = 'Dokumentera fastighetsskador'
        ordering = ['-date']
    
        
  

class Allergen(models.Model):
    name = models.CharField(max_length=30, verbose_name='Namn')
    description = models.TextField(max_length=200, blank=True, verbose_name='Beskrivning',
                                   help_text = """Kort beskrivning om allergenen, hur sprids den?
                                   Vart finns den? Vilka besvär skapar den?""")
    hazard = models.ForeignKey(
        Hazard,
        on_delete=models.PROTECT,
        verbose_name='Fara'
        )
    
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
        related_name='employee',
        verbose_name='signatur'
        )
    
    class Meta:
        verbose_name = 'produktion'
        verbose_name_plural = 'produktion'
        ordering = ['date']