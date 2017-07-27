from django.contrib import admin
from database.models import *
from Economy.models import Staff, Employee
from database.forms import BikesForm, AdminLunchBookingForm, CreateAvailableBikeForm,\
    BikeBookingForm, AdminGuestForm
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from database.helperfunctions import create_date_list
from datetime import timedelta

# register bikes for users
class DamagesInline(admin.TabularInline):
    model = Damages
    extra = 1
    
#@admin.register(BikeSize)
class BikeSizeAdmin(admin.ModelAdmin):
    fields = ['name', 'internal', 'wheelsize', 'min_age', 'max_age']
    
@admin.register(Bike)
class BikesAdmin(admin.ModelAdmin):
    form_class = BikesForm
    list_display = ['number', 'bikeKeyNo','size', 'damage_report']
    
    readonly_fields = ['damage_report',]
    inlines = (DamagesInline, )
    
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
    fields = ['name', 'type', 'price' ,'slug']
    list_display = ['name', 'type', 'price' ,'slug']
    
@admin.register(Targetgroup)   
class TargetGroupAdmin(admin.ModelAdmin):
    fieldsets=[
        (None,      {'fields': ['name']}),
        ('Beteenden',{'fields': ['behaviour', 'values', 'buys']})
        ]
    list_display = ['name']
    
class DayInline(admin.TabularInline):
    model = Day
    fieldsets=[
        (None,      {'fields': ['order']}),
        ('Innehåll',{'fields': ['include_adultbike', 'include_childbike', 'room', 'lunch', 'dinner']}),
        ('Texter',  {'fields': ['distance', 'locks', 'text', 'image', 'image_alt']})
        ]
    extra = 0
    
@admin.register(Package)   
class PackageAdmin(admin.ModelAdmin):
    fieldsets=[
        (None,          {'fields': ['slug', 'title', 'active', 'price', 'vat25', 'vat12']}),
        ('Målgrupper',  {'fields': ['targetgroup']}),
        ('Texter',      {'fields': ['ingress', 'image', 'image_alt']}),
    ] 
    inlines = [DayInline, ]
    list_display = ['title', 'slug', 'active', 'price', 'targetgroup']
    
'''
Booking admin
Huvudadminen BookingAdmin som enbart är tänkt att användas. Alla andra typer av bokningar
sker genom inlines i denna.
'''    
# Inlines
class RoomsBookingInLine(admin.TabularInline):
    model = RoomsBooking
    extra = 1
    fields = ['numberOfGuests', 'from_date', 'to_date', 'room', 'subtotal']
    readonly_fields = ['subtotal',]
        
class BikesBookingInLine(admin.TabularInline):
    model = BikesBooking
    form = BikeBookingForm
    extra = 0
    readonly_fields = ['to_date', 'subtotal']
    
class LunchBookingInLine(admin.TabularInline):
    model = LunchBooking
    extra = 1
    form = AdminLunchBookingForm
    readonly_fields = ['subtotal']


        
@admin.register(Booking)
class BookingsAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,          {'fields': ['guest', 'booking', 'package', 'status', 'longest_prel', 'created_at', 'updated_at']}),
        ('Info om gästen', {'fields': ['adults', 'children', 'discount_code']}),
        ('Specifikationer', {'fields': ['total', 'booked_bike_report', 'booked_room_report',
                                        'booked_lunch_report']}),
        ]
    list_display = ['booking', 'status', 'guest', 'start_date', 'total', 'created_at', 'updated_at','adults', 'children']
    list_filter = ['created_at', 'status']
    search_fields = ['booking', 'guest__first_name', 'guest__last_name', 'guest__email']
    readonly_fields = ['created_at', 'updated_at', 'booked_bike_report', 'booked_room_report',
                       'booked_lunch_report', 'total', 'status', 'longest_prel']
    actions = ['cancel_booking', 'preliminary', 'make_active', 'complete']
    inlines = [BikesBookingInLine, RoomsBookingInLine, LunchBookingInLine]
    
    # REPORTS
    def start_report(self, instance):
        dates = [bikes.from_date for bikes in instance.booked_bike.all()]
        if not None in dates and dates != []:
            dates.sort()
            stdate = dates[0]
        else:
            stdate = None
        return '{}'.format(stdate)
    start_report.short_description = 'Startdatum'
    
    def booked_bike_report(self, instance):
        return format_html_join(mark_safe('<br>'),
                                'Typ: {}cykel, Nummer: {}',
                                ((str(bike.bike.attribute), str(bike.bike.number, )) for bike in instance.booked_bike.all()
                                ) or mark_safe("<span class='errors'>Det finns inga cykelbokningar registrerade hos denna bokning</span>")
                                )
    booked_bike_report.short_description = 'Cyklar för denna bokning'
    
    def booked_room_report(self, instance):
        return format_html_join(mark_safe('<br>'),
                                'Rum: {}, Antal personer: {}, Incheckning: {}, Utcheckning: {}',
                                ((str(room.room), str(room.numberOfGuests), str(room.from_date), str(room.to_date), ) for room in instance.booked_rooms.all()
                                ) or mark_safe("<span class='errors'>Det finns inga rumsbokningar registrerade hos denna bokning</span>")
                                )
    booked_room_report.short_description = 'Rum för denna bokning'
    
    def booked_lunch_report(self, instance):
        return format_html_join(mark_safe('<br>'),
                                'Typ: {}, Antal: {}, Dag:{}',
                                ((str(lunch.type), str(lunch.quantity), str(lunch.day),  ) for lunch in instance.booked_lunches.all()
                                ) or mark_safe("<span class='errors'>Det finns inga luncher bokade i denna bokning</span>")
                                )
    booked_lunch_report.short_description = 'Luncher för denna bokning'
    
    # ACTIONS
    def cancel_booking(self, request, queryset):
        for item in queryset:
            bk_books = BikesBooking.objects.filter(booking=item.booking)
            for bk in bk_books:
                for day in create_date_list(bk.from_date, bk.duration.days):
                    BikeAvailable.objects.unbook_bike(bk.bike, day)
                bk.bike = None
                bk.save()
        queryset.update(status='cancl')
    cancel_booking.short_description = 'Avboka'
    
    def preliminary(self, request, queryset):
        for item in queryset:
            item.longest_prel = item.start_date - timedelta(days=1)
            item.save()
        queryset.update(status = 'prel')
    preliminary.short_description = 'Gör till preliminärbokning'
    
    def make_active(self, request, queryset):
        for item in queryset:
            item.save()
        queryset.update(status='actv')
        
    make_active.short_description = 'Gör aktiv'
    
    def complete(self, request, queryset):
        '''
        Potentiell hook för att bygga på utvärdering från gästerna.
        '''
        queryset.update(status='cmplt')
    complete.short_description = 'Markera som genomförd'
    
    def confirm_booking(self, request, queryset):
        queryset.update(status= 'conf')
    confirm_booking.short_description = 'Bekräfta bokning'

    # GETTERS
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super(BookingsAdmin, self).get_readonly_fields(request, obj)
        else:
            return self.readonly_fields + ['booking']
    
@admin.register(RoomsBooking)
class RoomsBookingAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,          {'fields': ['booking', 'numberOfGuests', 'room']}),
        ('datum',       {'fields': ['from_date', 'to_date']}),
        ('pris',        {'fields': ['subtotal']}),
        ]
    list_display = ['booking', 'numberOfGuests', 'room', 'subtotal','from_date', 'to_date']
    readonly_fields = ['subtotal']
    
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
    
@admin.register(GuestProfile)
class GuestAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,        {'fields': ['first_name', 'last_name', 'email', 'phone_number', 'newsletter']}),
        ('Info',      {'classes': ('collapse', ),
                       'fields': ['date_joined']}),
        ]
    
    readonly_fields = ['date_joined']
    list_display = ['first_name', 'last_name', 'email', 'phone_number', 'newsletter']

    
admin.site.disable_action('delete_selected')
admin.site.unregister(User)
admin.site.register(Employee, StaffAdmin)
admin.site.register(User)