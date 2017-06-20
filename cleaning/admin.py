from django.contrib import admin
from cleaning.forms import *
from cleaning.models import *

from django.core.exceptions import ValidationError
from django.contrib.contenttypes.admin import GenericTabularInline
'''
TODO:
* Färdigställ utifrån modellen
* Lägg till fält i admin-vyn där dagens, morgonens och att-göra uppgifter syns

'''
class RiskAnalysisInline(admin.TabularInline):
    model = RiskAnalysis
    fields = ['control_point', 'routine', 'routine_recurr', 'routine_sufficient', 'comment']
    extra = 0
    verbose_name = 'Rutin'
    
class ControlPointInline(GenericTabularInline):
    model = ControlPoint
    
@admin.register(Routine)
class RoutineAdmin(admin.ModelAdmin):
    form = RoutineForm
    fieldsets = [
        (None,      {'fields':['name', 'created', 'updated', 'purpose']}),
        ('Beskrivning', {'fields':['description']}),
        ('Vid avvikelse', {'fields':['monitoring', 'anomaly_measure', 'anomaly_correction']}),
        #('Kontrollpunkter', {'fields': ['control_points']}),
        ]
    readonly_fields = ['created', 'updated']
    list_display = ['name', 'created', 'updated']
    
@admin.register(Hazard)
class HazardAdmin(admin.ModelAdmin):
    form = HazardForm
    fieldsets = [
        (None,              {'fields':['name']}),
        ('Kategorisering',  {'fields': ['type', 'how']}),
        ('Beskrivning',     {'fields': ['description']}),
        ('Analys',          {'fields': ['analysis']}),
        ]
    list_display= ['name', 'type', 'how']
    
@admin.register(ColdStorage)
class ColdStorageAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields':['name', 'created', 'updated']}),
        ('Grunder',         {'fields':['active', 'location', 'short_description']}),
        ('Temperaturer',    {'fields': ['number', 'kind', 'prescribedMaxTemp', 'prescribedMinTemp']}),
        ('Riskanalys',      {'fields':['hazard', ]}),
        ]
    readonly_fields = ['created', 'updated']
    list_display = ['name', 'number', 'active', 'kind', 'created', 'updated']
    inlines = [RiskAnalysisInline]
    
@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields':['name', 'created', 'updated']}),
        ('Grunder',         {'fields':['active', 'location', 'short_description']}),
        ('Riskanalys',      {'fields':['hazard',]}),
        ]
    readonly_fields = ['created', 'updated']
    list_display = ['name', 'active', 'created', 'updated']
    inlines = [RiskAnalysisInline]
    
@admin.register(Preparation)
class PreparationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields':['name', 'created', 'updated']}),
        ('Grunder',         {'fields':['active', 'location', 'short_description']}),
        ('Riskanalys',      {'fields':['hazard',]}),
        ]
    readonly_fields = ['created', 'updated']
    list_display = ['name', 'active', 'created', 'updated']
    inlines = [RiskAnalysisInline]
    
@admin.register(Serving)
class ServingAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields':['name', 'created', 'updated']}),
        ('Grunder',         {'fields':['active', 'location', 'short_description']}),
        ('Riskanalys',      {'fields':['hazard',]}),
        ]
    readonly_fields = ['created', 'updated']
    list_display = ['name', 'active',  'created', 'updated']
    inlines = [RiskAnalysisInline]
    
@admin.register(CriticalControlPoint)
class CriticalControlPointAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields':['name', 'created', 'updated']}),
        ('Grunder',         {'fields':['active', 'location', 'short_description']}),
        ('Riskanalys',      {'fields':['hazard',]}),
        ('Extra riskminimering', {'fields': ['extra_monitoring', 'upper_limit',
                                             'lower_limit']}),
        ]
    readonly_fields = ['created', 'updated']
    list_display = ['name', 'active', 'created', 'updated']
    inlines = [RiskAnalysisInline]
    
@admin.register(Temperature)
class TemperatureAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['control_point', 'date', ]}),
        ('Kontroll',        {'fields': ['measured', 'measure']}),
        ('Signering',       {'fields': ['signature', 'comment']})
        ]
    list_display = ['control_point', 'date', 'anomaly', 'signature']
    list_filter = ['anomaly']
    #search_fields = ['control_point', 'date', 'signature']
    
    def save_model(self, request, obj, FridgeControlForm, change):
        higher = obj.measured > obj.control_point.prescribedMaxTemp
        lower = obj.measured < obj.control_point.prescribedMinTemp

        # Check for anomaly
        if higher or lower:
            obj.anomaly = True
        else:
            obj.anomaly = False   
        obj.save()
            
@admin.register(Clean)
class CleanAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['date', ]}),#'control_point'
        ('Kontroll',        {'fields': ['cleaned', 'anomaly', 'measure']}),
        #('Signering',       {'fields': ['signature', 'comment']})
        ]
    #list_display = ['control_point', 'date', 'anomaly', 'signature']
    
    
@admin.register(FacilityDamage)
class FacilityDamageAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['location', 'date' ]}),
        ('Kontroll',        {'fields': ['description', 'measure']}),
        ('Signering',       {'fields': ['repaired', 'signature', 'comment']})
        ]
    list_display = ['location', 'date', 'anomaly', 'signature']

        
@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['supplier', 'date', 'note']}),
        ('Genomgång',       {'fields': ['smell', 'damaged', 'expired']}),
        ('Signering',       {'fields': ['signature']}),
        ]

    list_display = ['supplier', 'date', 'note', 'anomaly', 'signature']

    def save_model(self, request, obj, form, change):
        if not obj.smell or not obj.damaged or not obj.expired:
            obj.anomaly = True
        else:
            obj.anomaly = False
        obj.save()
        
@admin.register(Allergen)
class AllergenAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields':['name']}),
        ('Beskrivning',     {'fields':['description', 'hazard']}),
        ]
    list_display = ['name']
    
@admin.register(Ingredience)
class IngredienceAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['name', 'price', 'package_size']}),
        ('övrigt',          {'fields': ['allergen', 'supplier']}),
        ]
    list_display = ['name', 'supplier']
    list_filter = ['supplier', 'allergen']
    
class IngredienceInline(admin.TabularInline):
    model = RecepieIngredience
    fields = ['ingredience', 'amount']
    
@admin.register(Recepie)
class RecepieAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['name', 'added', 'updated']}),
        ('Priser',          {'fields': ['customer_price', 'retailer_price', 'pieces',
                                        ]}),
        ('Produktion',      {'fields': ['work_hours', 'oven_time', 'description']})
        ]
    readonly_fields = ['added', 'updated']
    inlines = [IngredienceInline]
    list_display = ['name', 'customer_price', 'retailer_price', 'pieces', 'work_hours']
    
@admin.register(Production)
class ProductionAdmin(admin.ModelAdmin):
    fields = ['recepie', 'amount', 'date', 'signature']
    list_display = ['recepie', 'amount', 'date', 'signature']
    
    list_filter = ['recepie', 'date', 'signature']
    
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['name', 'contact', 'phone', 'email']}),
        ('Beställningar',   {'fields': ['order_day']}),
        ('Beskrivning',     {'fields': ['description', 'other']}),
        ]
    list_display = ['name', 'contact', 'phone', 'email', 'order_day']