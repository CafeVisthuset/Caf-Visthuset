from functools import update_wrapper

from django.contrib import admin
from .models import Bike, Booking, BikeAvailable, BikesBooking, LunchBooking
from database.models import Damages, Facility, Rooms, Guest, RoomsBooking, Lunch
from Economy.models import Staff, Employee
from database.forms import BikesForm, LunchBookingForm, CreateAvailableBikeForm,\
    BikeBookingForm
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User



# register bikes for users
class DamagesInline(admin.TabularInline):
    model = Damages
    extra = 1
    
@admin.register(Bike)
class BikesAdmin(admin.ModelAdmin):
    form_class = BikesForm
    list_display = ('number', 'attribute', 'wheelsize','rentOutCount', 'damage_report')
    
    readonly_fields = ['damage_report', 'rentOutCount']
    inlines = (DamagesInline, )
    
    actions = ['reset_rent_out_count', ]  
    
    # Actions
    def reset_rent_out_count(self, request, queryset):
        queryset.update(rentOutCount = 0)
    reset_rent_out_count.short_description = 'Återställ antal uthyrningar till 0'

    # Readonly outputs
    def damage_report(self, instance):
        return format_html_join(mark_safe('<br/>'),
                                '{}',
                                ((line, ) for line in instance.damages.filter(repaired = 'False').all()
                                ) or mark_safe(
                                    "<span class='errors'>I can´t determine this adress</span>"))
    damage_report.short_description = 'Aktuella skador'

@admin.register(Damages)
class DamagesAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,      {'fields': ['bike_id', 'discoveredDate', 'discoveredBy']}),
        ('Beskrivning', {'fields': ['damageType', ]}),
        ('Lagning',     {'fields': ['repaired', 'repairedBy', 'repairedDate'],
                         'classes': ['collapse', ]}),
        ]
    
    list_display = ['bike_id', 'discoveredDate', 'repaired', 'repairedDate', 'repairedBy']

@admin.register(BikeAvailable)
class BikesAvail(admin.ModelAdmin):
    list_display = ['bike', 'available_date', 'available', 'bookings']
    
'''
Admins for rooms and facilities
'''
class RoomsInline(admin.TabularInline):
    model = Rooms
    extra = 0

@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    # form = AccomodationForm
    fieldsets = [(None,      {'fields': ['name', 'organisation_number']}),
                 ('Kontaktuppgifter', {'fields': ['email', 'telephone', 'website']}),
                 ('Adress',  {'fields': ['adress', 'postCode', 'location']}),
                 ('Rum',     {'fields': ['rooms_report']}),
                 ('För hemsidan',   {'fields': ['slug']}),
                 ]
    list_display = ['name', 'email', 'telephone','website', 'adress_report', ]
    
    readonly_fields = ('adress_report', 'rooms_report')
    inlines = (RoomsInline, )
    
    def adress_report(self, instance):
        return format_html_join(
            mark_safe('<br/>'),
            '{}',
            ((line, ) for line in instance.get_full_adress()),
            ) or mark_safe("<span class='errors'>I can´t determine this adress</span>")
    adress_report.short_description = 'Adress'
    
    def rooms_report(self, instance):
        return format_html_join(mark_safe('<br/>'),
                                '{}',
                                ((line, ) for line in instance.rooms.all())
                                ) or mark_safe("<span class='errors'>Det finns inga registrerade rum hos denna anläggning</span>")

    rooms_report.short_description = 'Anläggningens rum'

@admin.register(Rooms)
class RoomsAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,          {'fields': ['name', 'number', 'owned_by', 'standard']}),
        ('Specifikationer',     {'fields': ['max_guests', 'price']}),
        (None,          {'fields': ['describtion']}),
        ]
    
    list_display = ['name', 'owned_by', 'standard', 'max_guests', 'price', ]


'''
Admins for Lunch and Utilities

'''
@admin.register(Lunch)
class LunchAdmin(admin.ModelAdmin):
    fields = ['type', 'price' ,'slug'] 



'''
Booking admins

TODO:
# Gör funktion för att räkna ut totalpris
# Gör totalpris till readonly
# Beräkna subtotal i varje bokningsmodell

'''    
# Inlines
class RoomsBookingInLine(admin.TabularInline):
    model = RoomsBooking
    extra = 1
    fields = ['numberOfGuests', 'from_date', 'to_date', 'room', 'subtotal']
    readonly_fields = ['subtotal']
    

    
class BikesBookingInLine(admin.TabularInline):
    model = BikesBooking
    form = BikeBookingForm
    extra = 0
    readonly_fields = ['subtotal']
    
class LunchBookingInLine(admin.TabularInline):
    model = LunchBooking
    extra = 1
    form = LunchBookingForm
    readonly_fields = ['subtotal']

    
@admin.register(Booking)
class BookingsAdmin(admin.ModelAdmin):
    
    fieldsets = [
        (None,          {'fields': ['guest', 'booking', 'created_at', 'updated_at']}),
        ('Info om gästen', {'fields': ['adults', 'children', 'discount_code']}),
        ('Specifikationer', {'fields': ['total', 'booked_bike_report', 'booked_room_report',
                                        'booked_lunch_report']}),
        ]
    list_display = ['booking', 'guest', 'total', 'created_at', 'updated_at','adults', 'children']
    readonly_fields = ['booking', 'created_at', 'updated_at', 'booked_bike_report', 'booked_room_report',
                       'booked_lunch_report', 'total']
    
    
    inlines = [BikesBookingInLine, RoomsBookingInLine, LunchBookingInLine]
    def booked_bike_report(self, instance):
        return format_html_join(mark_safe('<br/>'),
                                'Typ: {}cykel, Nummer: {}',
                                ((str(bike.bike.attribute), str(bike.bike.number, )) for bike in instance.booked_bike.all()
                                ) or mark_safe("<span class='errors'>Det finns inga cykelbokningar registrerade hos denna bokning</span>")
                                )
    booked_bike_report.short_description = 'Cyklar för denna bokning'
    
    def booked_room_report(self, instance):
        return format_html_join(mark_safe('<br/>'),
                                'Rum: {}, Antal personer: {}, Incheckning: {}, Utcheckning: {}',
                                ((str(room.room), str(room.numberOfGuests), str(room.from_date), str(room.to_date), ) for room in instance.booked_rooms.all()
                                ) or mark_safe("<span class='errors'>Det finns inga rumsbokningar registrerade hos denna bokning</span>")
                                )
    booked_room_report.short_description = 'Rum för denna bokning'
    
    def booked_lunch_report(self, instance):
        return format_html_join(mark_safe('<br/>'),
                                'Typ: {}, Antal: {}, Dag:{}',
                                ((str(lunch.type), str(lunch.quantity), str(lunch.day),  ) for lunch in instance.booked_lunches.all()
                                ) or mark_safe("<span class='errors'>Det finns inga luncher bokade i denna bokning</span>")
                                )
    booked_lunch_report.short_description = 'Luncher för denna bokning'
    
    
@admin.register(BikesBooking)
class BikesBookingAdmin(admin.ModelAdmin):
    form_class = BikeBookingForm
    #fieldsets = [
    #    (None,         {'fields': ['booking', ]}),
    #    ('Pris',        {'fields': ['subtotal']}),
    #    ]
    
    def available_bikes(self, instance):
        # Gör funktion som hämtar alla lediga cyklar
        pass

@admin.register(RoomsBooking)
class RoomsBookingAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,          {'fields': ['booking', 'numberOfGuests', 'room']}),
        ('datum',       {'fields': ['from_date', 'to_date']}),
        ('pris',        {'fields': ['subtotal']}),
        ]
    list_display = ['booking', 'numberOfGuests', 'room', 'subtotal','from_date', 'to_date']
    readonly_fields = ['subtotal']
    
    
@admin.register(LunchBooking)
class LunchBooking(admin.ModelAdmin):
    form_class = LunchBookingForm
    #fields = ['quantity', 'subtotal']


'''
Staff and guest admins. Belongs to auth app.
'''
class StaffAdmin(UserAdmin):
    fieldsets = [
        (None,      {'fields': ['username', 'password', 'last_login', 'date_joined']}),
        ('Personlig information', {'fields': ['first_name', 'last_name', 'email', 'phone_number']}),
        ('Ekonomiska uppgifter', {'fields': ['hours_worked', 'wage', 'tax', 'drawTax']}),
        ('Övrigt',      {'classes': ('collapse', ),
                        'fields': ['is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions']}),
        ]
    
    readonly_fields = ['last_login', 'date_joined', 'hours_worked']
    list_display = ['username', 'first_name', 'last_name', 'phone_number', 'hours_worked', 'wage',
                    'tax', 'drawTax']
    

class GuestAdmin(StaffAdmin):
    fieldsets = [
        (None,      {'fields': ['username', 'password', 'last_login', 'date_joined']}),
        ('Personlig information', {'fields': ['first_name', 'last_name', 'email', 'phone_number', 'newsletter']}),
        ('Övrigt',      {'classes': ('collapse', ),
                        'fields': ['is_active']}),
        ]
    
    readonly_fields = ['last_login', 'date_joined']
    list_display = ['username', 'first_name', 'last_name', 'phone_number', 'newsletter']

admin.site.unregister(User)
admin.site.register(Employee, StaffAdmin)
admin.site.register(Guest, GuestAdmin)
admin.site.register(User)