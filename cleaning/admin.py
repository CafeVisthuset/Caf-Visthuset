from django.contrib import admin
from cleaning.forms import *
from cleaning.models import *
'''
TODO:
* Färdigställ utifrån modellen
* Lägg till fält i admin-vyn där dagens, morgonens och att-göra uppgifter syns

'''
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['name', 'contact', 'phone', 'email']}),
        ('Beställningar',   {'fields': ['order_day']}),
        ('Beskrivning',     {'fields': ['description', 'goods', 'other']}),
        ]
    list_display = ['name', 'contact', 'phone', 'email', 'order_day']
    
    
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
@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['supplier', 'date']}),
        ('Genomgång',       {'fields': ['damaged', 'expired']}),
        ('Signering',       {'fields': ['signature']}),
        ]
    list_display = ['supplier', 'date', 'anomaly', 'signature']
    
@admin.register(Allergen)
class AllergenAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields':['name']}),
        ('Beskrivning',     {'fields':['describtion', 'hazard']}),
        ]
    list_display = ['name']
    
@admin.register(Ingredience)
class IngredienceAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['name', 'price', 'package_size']}),
        ('övrigt',          {'fields': ['allergen', 'supplier']}),
        ]
    list_display = ['name', 'supplier']
    
class IngredienceInline(admin.TabularInline):
    model = RecepieIngredience
    fields = ['ingredience', 'amount']
    
@admin.register(Recepie)
class RecepieAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['name']}),
        ('Priser',          {'fields': ['customer_price', 'retailer_price', 'pieces'
                                        'work_hours']}),
                 
        ]
    inlines = [IngredienceInline]
    list_display = ['name', 'customer_price', 'retailer_price', 'pieces', 'work_hours']
    
