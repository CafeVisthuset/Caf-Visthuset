from django.db import models
from datetime import date
from Economy.models import Employee

"""
TODO:
* Lägg in rutiner för städning och koll av temperaturer
    # Om aktiv, skicka påminnelser, annars inte
    # Om Visthuset har öppet, skicka påminnelser om städning, annars inte
* Lägg in alla möjliga kontrollpunkter
    # Förråd
    # Golv
    # Alternativt: lägg in en stor modell som passar alla områden och
      lägg in alla kontrollpunkter där
* Lägg in verbose_name för alla fält
* Lägg in databas över recept, ingredienser och allergener
    # Product är en Abstract Model
    # Ingredient och Allergen är båda Products med en OneToOne-relation
    # Recepies har en egen modell med en ManyToMany-relation med ingrediens
        -receptet har både en ingredienslista och en instruktionslist
        -instruktionslista är egen modell, isåfall finns egen textmodell
        där även flatpages ingår. Ett fält anger vilken typ av text det är.
* Lägg in beställningsrutiner och telefonnumer, eventuellt som en flatpage
* Lägg in schema för personalen 
"""
# Model to store info on Freezers
class Freezer(models.Model):
    type = models.CharField(max_length = 50, verbose_name='Typ av frys')
    location = models.CharField(max_length = 255, verbose_name='Plats')
    active = models.BooleanField(default=True, verbose_name='Är den aktiv?')
    
    def __str__(self):
        return "%s, %s" % (self.type, self.location)
    
    class Meta:
        verbose_name = 'Frys'
        verbose_name_plural = 'Frysar'
        ordering = ['-active']

# Model to store info on fridges        
class Fridge(models.Model):
    type = models.CharField(max_length = 50, verbose_name='Typ av kyl')
    location = models.CharField(max_length = 255, verbose_name='Plats')
    active = models.BooleanField(default=True, verbose_name='Är den aktiv?')
    
    def __str__(self):
        return "%s, %s" % (self.type, self.location)
    
    class Meta:
        verbose_name = 'Kyl'
        verbose_name_plural = 'Kylar'
        ordering = ['-active']

# Abstract model for holding info on temperatures
class Temperature(models.Model):
    measured = models.IntegerField(verbose_name='Uppmätt temperatur')
    defrosted = models.BooleanField(default=False, verbose_name='Avfrostad')
    anomaly = models.BooleanField(default=False, verbose_name='avvikelse')
    cleaned = models.BooleanField(verbose_name='Städat')
    comment = models.TextField(max_length=255, blank=True, verbose_name='kommentar')
    prescribedMaxTempFridge = models.PositiveIntegerField(default= 8)
    prescribedMinTempFridge = models.PositiveIntegerField(default= 4)
    prescribedMaxTempFreezer = models.IntegerField(default= -4)
    prescribedMinTempFreezer = models.IntegerField(default= -20)

    class Meta:
        abstract = True
        
# Model to store temperatures for fridges        
class FridgeTemp(Temperature):
    unit = models.ForeignKey(
        Fridge,
        on_delete=models.PROTECT,
        verbose_name = 'Enhet',
        to_field= 'id',
        limit_choices_to={'is_active': True}
        )
    date = models.DateField(default=date.today, verbose_name='datum')
    signature = models.ForeignKey(
        Employee,
        verbose_name = 'Signatur'
        )
    
    class Meta:
        verbose_name = 'Kontrollpunkt kylskåp'
        verbose_name_plural ='Kontrollpunkter kylskåp'
        ordering = ['date']
        
# Model to store temperatures for Freezers
class FreezerTemp(Temperature):
    unit = models.ForeignKey(
        Freezer,
        on_delete=models.PROTECT,
        verbose_name='Typ av frys',
        limit_choices_to={'active': True},
        )
    date = models.DateField(default=date.today)
    signature = models.ForeignKey(
        Employee,
        verbose_name= 'Signatur'
        )
    
    class Meta:
        verbose_name = 'Kontrollpunkt frys'
        verbose_name_plural = 'Kontrollpunkter frysar'
        ordering = ['-date']
        


# Abstract model to store basic info on cleaning routines        
class Clean(models.Model):
    clean = models.BooleanField(default=False)
    open = models.BooleanField(default=True)
    date = models.DateField(default=date.today)
    
    class Meta:
        abstract = True
        ordering = ['date']
        
    def open_visthuset(self):
        if not self.open:
            self.open = True
            return self.open
        else:
            self.open = False
        return self.open
    
# Model for updating when a larger cleaning was last done in the kitchen
class Kitchen(Clean):
    signature = models.ForeignKey(
        Employee,
        )
    
    class Meta:
        verbose_name = 'Köket'

class Floor(Clean):
    signature = models.ForeignKey(
        Employee,
        )
    
    class Meta:
        verbose_name = 'Golv'
        verbose_name_plural = 'Golven'
        
