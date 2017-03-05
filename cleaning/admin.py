from django.contrib import admin
from cleaning.forms import *
'''
TODO:
* Färdigställ utifrån modellen
* Lägg till fält i admin-vyn där dagens, morgonens och att-göra uppgifter syns

'''

@admin.register(Fridge)
class FridgeAdmin(admin.ModelAdmin):
    fields = ['type', 'location', 'active']
    list_display = ['type', 'location', 'active']
    form = FridgeForm
    
@admin.register(Freezer)
class FreezerAdmin(admin.ModelAdmin):
    fields = ['type', 'location', 'active']
    list_display = ['type', 'location', 'active']
    display_radio=['active']
    form = FreezerForm
    
@admin.register(FridgeTemp)
class FridgeControl(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['date', 'unit']}),
        ('Temperaturer',    {'fields': ['measured']}),
        ('Rengöring',      {'fields': ['cleaned']}),
        ('Signering',       {'fields': ['signature']}),
        ]
    list_display = ['date', 'unit', 'signature', 'anomaly']
    empty_value_display = 'Okänt'
    form = FridgeControlForm
    
    def save_model(self, request, obj, FridgeControlForm, change):
        higher = obj.measured > obj.prescribedMaxTempFridge
        lower = obj.measured < obj.prescribedMinTempFridge
        if higher or lower:
            obj.anomaly = True
            obj.save()
        else:
            obj.anomaly = False   
            obj.save()
    
@admin.register(FreezerTemp)
class FreezerControl(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['date', 'unit']}),
        ('Temperaturer',    {'fields': ['measured']}),
        ('Rengöring',      {'fields': ['cleaned', 'defrosted'] }),
        ('Signering',       {'fields': ['signature']}),
        ]
    list_display = ['date', 'unit', 'signature', 'anomaly']
    form = FreezerControlForm
    
    def save_model(self, request, obj, FridgeControlForm, change):
        higher = obj.measured > obj.prescribedMaxTempFreezer
        lower = obj.measured < obj.prescribedMinTempFreezer
        if higher or lower:
            obj.anomaly = True
            obj.save()
        else:
            obj.anomaly = False   
            obj.save()
