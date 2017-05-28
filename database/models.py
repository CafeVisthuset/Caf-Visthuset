from django.db import models
from Economy.models import Employee
from .choices import *
from .validators import validate_booking_date, validate_preliminary
from datetime import date, timedelta, datetime
from django.core.exceptions import ValidationError, ObjectDoesNotExist,\
    MultipleObjectsReturned
from django.contrib.auth.models import User
from django.db.models import Q
from database.helperfunctions import listSum, create_date_list
from django.template.defaultfilters import last
from django.db.models.deletion import DO_NOTHING

'''
TODO:
* Gör klart alla modeller för att kunna genomföra bokningar
    # Gör det möjligt att föra statistik över sålda paket
    
* Lägg in modeller för generiska bokningar/eventbokningar

'''

class Targetgroup(models.Model):
    name = models.CharField(max_length=32, verbose_name='Namn på målgrupp')
    behaviour = models.TextField(max_length=1000, verbose_name='Beteende',
                                 help_text='Hur beter sig målgruppen i övrigt? Ex. Är de aktiva/livsnjutare?')
    values = models.TextField(max_length=1000, verbose_name='Värderingar',
                              help_text='Vad har de för värderingar?')
    buys = models.TextField(max_length=1000, verbose_name='Vad köper de annars?')
    
    class Meta:
        verbose_name = 'Målgrupp'
        verbose_name_plural = 'Målgrupper'
        
    def __str__(self):
        return self.name
'''
Models for lunches and lunch utilities
'''
class Lunch(models.Model):
    slug = models.SlugField(default='')
    type = models.CharField(choices=Lunch_Choices, default='vegetarian', max_length= 15, verbose_name='lunchalternativ')
    price = models.PositiveIntegerField(default = 95, verbose_name='pris')
    # TODO: implement allergens with lunches
    
    class Meta:
        verbose_name = 'lunch'
        verbose_name_plural = 'luncher'
        
    def __str__(self):
        return self.type

        
class Utilities(models.Model):
    describtion = models.TextField()
    number = models.PositiveIntegerField()
    brand = models.CharField(max_length=5, choices=Brand_choices)
    
    class Meta:
        verbose_name= 'tillbehör'
        

'''
Bike models

Contain a model for bike availability(BikeAvailable) with manager (BikeAvailableManager)
and model for bikes (Bike). It also contains a model for bike extras such as childseats.
Additionally this section contains a model for damages on each bike (Damages).
'''
class BikeManager(models.Manager):
    
    def adult_bikes(self):
        return super(BikeManager, self).adult_bikes().filter(
            Q(attribute='adult'))

class BikeBookingManager(models.Manager):
    """
    Manager to handle all bike bookings.
    
    :: get_available
    :: book_bike
    :: unbook_bike
    """
    
    def get_available(self, biketype, date_list):
        '''
        Method that takes a biketype and a date_list and returns
        a list with all the bike objects that are available for 
        the dates in the list.
        '''
        bikeset = self.filter(biketype)
        bks = []
        success_report = []
        for bike in bikeset:
            datelst = []
            succs = []
            # Iterate over the dates and find get the availability for the bike
            # each date. Also get False success if the bike is not in BikeAvailable
            # for that day.
            for date in date_list:
                avble, success = BikeAvailable.objects.bike_available_for_date(bike, date)
                
                datelst.append(avble)
                succs.append(success)
                
            # Append reporting    
            report = False in succs
            success_report.append(report)
            
            # If all the dates are available, put the bike in the list to return  
            if not False in datelst:
                bks.append(bike)

        return bks
    
    def book_bike(self, bike, date):
        '''
        Method that takes in a bike object and a date and book the bike
        by setting the available False
        '''
        pass
    
    def unbook_bike(self, bike, date):
        pass
    
# Bike model
class Bike(models.Model):
    number = models.PositiveIntegerField(verbose_name= 'Nummer')
    bikeKeyNo = models.CharField(max_length= 15, blank= True, verbose_name='Cykelnyckel')
    rentOutCount = models.IntegerField(default = 0, verbose_name='antal uthyrningar')
    wheelsize = models.CharField(choices=Bike_Wheelsize_Choices, max_length= 10,
                                 verbose_name='Däckdiameter')
    attribute = models.CharField(choices=Bike_Attribute_Choices, max_length= 10,
                                 verbose_name='vuxen/barn')
    extra = models.CharField(choices=Bike_Extra_Choices, max_length= 15,
                             verbose_name='Knuten till tillbehör', blank=True)
    
    objects = models.Manager()
    booking = BikeBookingManager()
    
    def __str__(self):
        attr = {
            'adult': 'vuxen',
            'young': 'ungdom',
            'child': 'barn',
            'smallChild': 'småbarn',
            }
        return "%scykel %s" % (attr[self.attribute], self.number)
    
    class Meta:
        verbose_name = 'cykel'
        verbose_name_plural = 'cyklar'
        ordering = ['-attribute', 'number']
        unique_together = ['number', 'attribute']

       
class BikeExtra(models.Model):
    name = models.CharField(max_length= 10, choices=Bike_Extra_Choices, verbose_name= 'cykeltillbehör')
    number = models.PositiveIntegerField(default= None, verbose_name= 'Nummer')
    attached_to = models.OneToOneField(
        Bike, 
        verbose_name= 'knuten till cykel',
        related_name= 'bikeextra',
        null = True,
        blank = True,
        )
    
    def __str__(self):
        return "%s %s" % (self.name, self.id)


class Damages(models.Model):
    bike_id = models.ForeignKey(
        Bike,
        on_delete=models.CASCADE,
        verbose_name= 'Skada på cykel',
        related_name= 'damages',
        )
    
    # Damage description
    discoveredBy = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        verbose_name = 'upptäckt av',
        related_name= 'discovered_by',
        blank=True,
        null = True,
        )
    discoveredDate = models.DateField(default=date.today, verbose_name='Skada upptäckt')
    repairedDate = models.DateField(default=date.today, verbose_name= 'Skada reparerad', blank=True)
    damageType = models.TextField(max_length = 200, verbose_name= 'beskrivning av skada' )
    
    # Repair status
    repaired = models.BooleanField(default = False, verbose_name = 'lagad (J/N)')   
    repairedBy = models.ForeignKey(
        'Economy.Employee',
        on_delete=models.CASCADE,
        blank = True,
        null = True,
        verbose_name= 'lagad av',
        related_name= 'repaired_by', 
        )
    
    def __str__(self):
        return self.damageType
    
    class Meta:
        verbose_name = 'skada'
        verbose_name_plural = 'skador'
        ordering = ['repaired', 'discoveredDate']


'''
Models for accomodation. Rooms and Facilities. 
'''
#Accomodation models
class Facility(models.Model):
    # Company
    name = models.CharField(max_length=30, verbose_name= 'boendeanläggning')
    organisation_number = models.CharField(max_length = 12, blank=True)
    
    # Contact details
    telephone = models.CharField(max_length=15, verbose_name='telefon', blank=True)
    email = models.EmailField(verbose_name='E-postadress')
    website = models.URLField(verbose_name='hemsida', blank=True)
   
    # Adress
    adress = models.CharField(max_length= 25, verbose_name= 'gatuadress', blank=True)
    postCode = models.CharField(max_length=8, verbose_name='postkod', blank=True)
    location= models.CharField(max_length=25, verbose_name='ort', blank=True)
   
    
    # For building URLs
    slug = models.SlugField(default='', blank=True)
    
    def __str__(self):
        return self.name
    
    def get_full_adress(self):
        return [self.adress, str(self.postCode) +'   ' + self.location]
    
    class Meta:
        verbose_name = 'boendeanläggning'
        verbose_name_plural = 'boendeanläggningar'
    
class Rooms(models.Model):
    # Title of room
    name = models.CharField(max_length=25, verbose_name='namn')
    number = models.PositiveIntegerField(blank= True)
    
    # Room attributes
    describtion = models.TextField(max_length=255, blank=True, verbose_name='Beskrivning')
    standard = models.CharField(choices=Room_Standard_Choices, max_length=20, verbose_name='standard')
    max_guests = models.PositiveIntegerField(verbose_name='Max antal gäster', default=4)
    
    # Price per room exkl. VAT
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0, 
                                verbose_name="pris exkl. moms",
                                help_text='Pris för rum exkl. moms')
    
    owned_by = models.ForeignKey(
        Facility,
        related_name= 'rooms',
        verbose_name='anläggning',
        null=True
        )
    
    class Meta:
        verbose_name = 'rum'
        verbose_name_plural = 'rum'
        ordering = ['owned_by']

    def __str__(self):
        return '%s, %s' % (self.name, self.owned_by.name)
        
'''
Models for packages. The package builds on a main Package-class which stores
all general info on the package and is called when booking. The Package class
has a one-to-many relation with the Day-class, which stores info about what is
included each day, as well as describing texts. The Package also has a Target-
group-class which stores information about which target group the package is aimed
at. This is only for internal use.
'''
class Package(models.Model):
    slug = models.SlugField(max_length=30, verbose_name='Internt namn', help_text='används i URL, använd inte åäö')
    title = models.CharField(max_length=40, verbose_name='Namn på paketet.')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Pris exkl. moms')
    vat25 = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Moms 25%')
    vat12 = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Moms 12%')
    targetgroup = models.ForeignKey(
        Targetgroup,
        blank=True,
        related_name='targetgroup',
        on_delete=models.DO_NOTHING,
        )
    ingress = models.TextField(max_length = 500)
    image = models.ImageField(upload_to='static/img/uploads/')
    image_alt = models.CharField(max_length=40, blank=True)
    
    def __str__(self):
        return self.title
    
class Day(models.Model):
    package = models.ForeignKey(
        Package,
        on_delete=DO_NOTHING,
        related_name='days',
        )
    order = models.PositiveIntegerField(verbose_name='Vilken dag?')
    adult_bike = models.PositiveIntegerField(help_text='Antal vuxencyklar', blank=True)
    child_bike = models.PositiveIntegerField(help_text='Antal barncyklar', blank=True)
    room = models.ForeignKey(
        Rooms,
        on_delete=models.DO_NOTHING,
        blank=True,
        )
    lunch = models.ForeignKey(
        Lunch,
        on_delete=models.DO_NOTHING,
        blank=True,
        related_name='lunch',
        )
    
    # Texts
    text = models.TextField(max_length=2000)
    image = models.ImageField(blank=True, upload_to='static/img/uploads/')
    image_alt =models.CharField(max_length=30, blank=True)
    distance = models.PositiveIntegerField(verbose_name='Hur långt cyklar man?', blank=True)
    locks = models.PositiveIntegerField(verbose_name='Hur många slussar?', blank=True)
    
    def __str__(self):
        return 'Dag {}, {}'.format(self.order, self.package)
    
'''
Guest model, inherits from GuestUser (Proxymodel of User) and GuestExtra
(abstract model with extra information that we want about the guests.

GuestUser also has an extended manager that sorts out guests from other users
'''
class GuestManager(models.Manager):
    
    def get_queryset(self):
        return super(GuestManager, self).get_queryset().exclude(
            Q(is_staff=True) | Q(is_superuser=True))
        
    def post_get_or_create(self, first_name, last_name, email, **kwargs):
        '''
        Gets or creates a guest user based on information passed from a booking form.
        '''
        try:
            # first try to find by email
            guest = Guest.objects.get(email=email)
        except MultipleObjectsReturned:
            # specify the search
            guest = Guest.objects.get(first_name=first_name, last_name=last_name, email=email)
            
        except ObjectDoesNotExist:
            # If the object doees not exist, create a new one
            password = User.objects.make_random_password()
            try:
                guest = Guest.objects.create(username=email, password=password, first_name=first_name,
                              last_name = last_name, email=email,
                              phone_number = kwargs['kwargs']['phone_number'],
                              newsletter = kwargs['kwargs']['newsletter'])
            except:
                # if the username is already taken, create a unique username for the person
                # this hopefully works, otherwise it fails.
                username= ','.join(['email', 'first_name', 'last_name'])
                guest = Guest.objects.create(username = username, password=password, first_name=first_name,
                              last_name = last_name, email=email,
                              phone_number = kwargs['kwargs']['phone_number'],
                              newsletter = kwargs['kwargs']['newsletter'])
                
        return guest
                     
class GuestExtra(models.Model):
    newsletter = models.BooleanField(default = True)
    phone_number = models.CharField(max_length=24, null=True, blank=True)
    
    class Meta:
        abstract = True
        
class GuestUser(User):
    class Meta:
        proxy = True
        
    
class Guest(GuestUser, GuestExtra):
    objects = GuestManager()
    
    class Meta:
        verbose_name = 'gäst'
        verbose_name_plural = 'gäster'
        
'''
Model and validator for discount code
'''
def validate_discount_code(value):
    found = False
    for item in Discount_codes.objects.all():
        if value == item.code:
            found = True
            break
        
    if found == False:
        raise ValidationError(
                '''rabattkoden verkar inte finnas i vårt system, 
                vänligen kontakta oss om problemet kvarstår'''
                )
        
class Discount_codes(models.Model):
    code = models.CharField(max_length=15, verbose_name= 'kod')
    value = models.DecimalField(decimal_places=2, max_digits=8)
    type = models.CharField(max_length=10, choices=Discount_Code_Choices)
    guest = models.ForeignKey(
        User,
        limit_choices_to={'is_guests': True},
        verbose_name = 'gäst',
        null = True
        )
'''
Booking models.

Model for booking, manager for booking querysets, helper function for
calculating booking_number, 
'''

def calc_booking_no():
    '''
    Returns a booking number for a new booking based on the date and the
    previous number of bookings the same day.
    '''
    try:
        # Normal case, should happen as long as database is not empty
        latest_booking = Booking.objects.latest('booking')
        bookingstr = str(latest_booking.booking)
        last_part = int(bookingstr[-2:])
    except Booking.DoesNotExist:
        # Catch an error if the database is empty, should only happen once
        last_part = 0
        bookingstr = '17010101'   # dummy variable
        print('Created the first booking in the database')
    
    # Start calculating the new booking number
    today = datetime.today()
    day_part = today.strftime('%y%m%d')
    booking_no = ''
    if bookingstr[:6] == day_part:
        last_part += 1
        if last_part <= 9:
            last_part = '0' + str(last_part)
        else:
            last_part = str(last_part)
        booking_no = day_part + str(last_part)
        return int(booking_no)
    else:
        booking_no = day_part + '01'
        return int(booking_no)

class BookingManager(models.Manager):
    '''
    Manager for managing bookings. Use this manager for all bookings!
    
    Ex of procedure for creating a booking.
    
    First call the manager to create a new instance of the booking-class
    1. Initiate booking,
        booking = Booking.book.create_booking(guest, start_date, end_date, 
                                    numberOfGuests, special request)
    
    Then update the booking instance and related instaces through the class
    methods.
    2. Set attributes of booking instance, use the class methods
        ex. booking.setBikeBooking()
        
    3. Get attributes for booking to be returned to user (optional)
        ex. booking.getBikeBooking(booking_number)
    
    # Basic functions
    :create_booking
    :update_booking
    :delete_booking
    :check_in_booking
    :check_out_booking
    # Getters
    :getBookingStatus
    :getBikeExtraBooking
    :getBikeBooking
    :getLunchBooking
    :getAccomodationBooking
     
    '''
    # Create, update, delete
    def create_booking(self, guest, start_date, end_date, adults, children, special_requests):
        return self.create(guest=guest,
                              start_date=start_date, 
                              end_date=end_date,
                              adults=adults,
                              children=children,
                              status='actv',
                              special_requests=special_requests)
        
    def update_booking(self, booking_number, **kwargs):
        booking = self.get(booking=booking_number)
        return booking.update(**kwargs)
        
    def delete_booking(self, booking, status_code):
        '''
        Make booking inactive with status code.
        '''
        pass
    
# Booking models
class Booking(models.Model):
    # Guest
    guest = models.ForeignKey(
        Guest,
        related_name='guest',
        on_delete=models.CASCADE,
        verbose_name='gäst',
        )
    
    # Booking specs
    booking = models.PositiveIntegerField(primary_key=True, verbose_name='boknings id', default=calc_booking_no)
    adults = models.IntegerField(null= False, default = 2, verbose_name='antal vuxna')
    children = models.IntegerField(null=True, default = 0, verbose_name='antal barn')
    special_requests = models.TextField(max_length = 255, null=True, blank= True, verbose_name= 'övrigt')
    
    # Fields for preliminary bookings
    longest_prel = models.DateTimeField(verbose_name='längsta preliminärbokning', null=True,
                                        validators= [validate_preliminary], blank=True)
    status = models.CharField(max_length=5, verbose_name='Status', choices=booking_status_codes)
    package = models.BooleanField(default=False, verbose_name='Paketbokning')
    # Dates
    start_date = models.DateField(verbose_name='datum för avresa', null=True, validators=
                                 [])
    end_date = models.DateField(verbose_name='datum för hemresa', null=True, validators=
                               [])
    
    # Potential discount code
    discount_code = models.CharField(blank=True, null=True, max_length=15, verbose_name= 'rabattkod',
                                     validators = [validate_discount_code])
    
    
    # Checked in/Checked out
    checked_in = models.BooleanField(default=False, verbose_name='incheckad (J/N)')
    checked_out = models.BooleanField(default=False, verbose_name='utcheckad(J/N)')
    
    # Economy
    total = models.DecimalField(decimal_places=2, max_digits=8)
    payed = models.BooleanField(default=False, verbose_name='betald')
    
    # When was the booking created
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)
    
    # Manager
    objects = models.Manager()
    book = BookingManager()
    
    class Meta:
        verbose_name = 'Bokning'
        verbose_name_plural = 'bokningar'
        ordering = ['-created_at', 'checked_in', 'start_date']
         
    def __str__(self):
        return str(self.booking)
    
    def save(self, *args, **kwargs):
        # Calculate total price for booking when saving
        priceList = []
        bikes = BikesBooking.objects.filter(booking=self.booking)
        [priceList.append(bike.subtotal) for bike in bikes]
        rooms = RoomsBooking.objects.filter(booking=self.booking)
        [priceList.append(room.subtotal) for room in rooms]
        lunches = LunchBooking.objects.filter(booking=self.booking)
        [priceList.append(lunch.subtotal) for lunch in lunches]
        
        self.total = listSum(priceList)
        super(Booking, self).save(*args, **kwargs)
        
        # create method that gathers all related bookings and calculates
        # the total price from their subtotals.
        
    # Methods to update specific parts of booking instances
    def check_in_booking(self):
        '''
        Check in guest. NEED TESTING
        '''
        self.checked_in = True
    
    def check_out_booking(self):
        '''
        Check out guest. NEED TESTING
        '''
        self.checked_out = True
    
    # Getters
    def getBookingStatus(self):
        '''
        Returns the status of the booking as a tuple. NEEDS TESTING!!
        '''
        return ('self.status', 
                self.checked_in,
                self.checked_out,
                self.payed)
        
    def getBikeBooking(self):
        return self.booked_bike
    
    def getLunchBooking(self):
        return self.booked_lunches
    
    # Setters
    def setBikeBooking(self, bike_list, start_date, end_date, duration):
        '''
        Checks if there are enough available bikes for the given dates.
        If there are enough bikes available, it will return True and a
        list of the bikes that are booked. Otherwise return False and a
        list of the available bikes it found. 
        '''
        for bike in bike_list:
            bike_booking = self.booked_bike.create(from_date=start_date, to_date=end_date, bike=bike)
            success = bike_booking.setBike(bike, create_date_list(start_date, duration.days))
        
            # If bike_booking is not created
            if bike_booking == None or not success:
                return False, None
        
        return True, bike_booking
    
    def destroyBikeBooking(self, bike, from_date, to_date):
        duration = to_date - from_date
        datelist = create_date_list(from_date, duration.days)
        for date in datelist:
            print(type(date))
            BikeAvailable.objects.unbook_bike(bike, date)
            

    def setBikeExtraBooking(self, **kwargs):
        pass
    
    def setLunchBooking(self, **kwargs):
        pass
    
    def setAccomodationBooking(self, **kwargs):
        pass

class BikesBooking(models.Model):
    # Dates and time
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()
    full_days = models.BooleanField(default=True)
    
    # Economy
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)
    
    # Bookings and specs
    bike = models.ForeignKey(Bike,
        related_name='bike',
        null = True,
        on_delete=models.DO_NOTHING,
        blank=True,
        #limit_choices_to = Bike.availability.fileter('available' = True),
        )
    booking = models.ForeignKey(
        Booking,
        related_name='booked_bike',
        on_delete=models.DO_NOTHING,
        db_index = True,
        )
    
    class Meta:
        verbose_name = 'cykelbokning'
        verbose_name_plural = 'cykelbokningar'
            
    def __str__(self):
        return str(self.booking)
    
    def save(self, *args, **kwargs):
        # Calculate price for bike booking and save
        days = self.to_date - self.from_date
        full_day = self.full_days
        price = 200
        self.subtotal = price * (days.days +1)
        super(BikesBooking, self).save(*args, **kwargs)
        '''
        # Update Available bikes
        numdays = self.to_date.day - self.from_date.day
        date_list = [(self.from_date + timedelta(days=x)) for x in range(0,numdays + 1)]
            
        [BikeAvailable.objects.book_bike(
            bike=self.bike, date=date, booking=self) for date in date_list]
        '''
        
    def setBike(self, bike, date_list):
        '''
        Books a bike in BikeAvailable and assign the bike to self instance
        
        Used in:
        setBikeBooking()
        '''
        for date in date_list:
            success = self.availableBike.book_bike(self, bike, date)
            if not success:
                return success
            
        self.bike = bike
        return success
        
    '''
    TODO:
    # Lägg in sökning för tillgängliga cyklar
    # Överväg att lägga med datum
    # Bygg modell i ekonomi för priser
    '''
        
class BikeExtraBooking(models.Model):
    # Dates and times
    from_date = models.DateTimeField()
    to_date = models.DurationField(choices=Day_Choices)
    full_day = models.BooleanField(default=True)
    
    # Booking specs
    extra = models.ForeignKey(
        BikeExtra,
        null=True,
        on_delete=models.CASCADE,
        related_name='bike_extra'
        )
    booking = models.ForeignKey(
        Booking,
        null = True,
        on_delete=models.CASCADE,
        related_name='Booking',
        )
    
    def __str_(self):
        return self.extra
    
    def save(self, *args, **kwargs):
        days = self.to_date - self.from_date
        #full_day = self.full_day
        price = 200
        self.subtotal = price * (days.days +1)
        super(BikesBooking, self).save(*args, **kwargs)
        

    
class RoomsBooking(models.Model):
    numberOfGuests = models.PositiveIntegerField(verbose_name='antal gäster')
    from_date = models.DateField()
    to_date = models.DateField()
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)
    booking = models.ForeignKey(
        Booking,
        related_name='booked_rooms',
        on_delete=models.CASCADE,
        )
    room = models.ForeignKey(
        Rooms,
        on_delete=models.CASCADE
        )
    
    class Meta:
        verbose_name = 'rumsbokning'
        verbose_name_plural = 'rumsbokningar'
    
    def __str__(self):
        return str(self.room)
    
    def save(self, *args, **kwargs):
        nights = self.to_date - self.from_date
        price = self.room.price
        self.subtotal = price * nights.days
        super(RoomsBooking, self).save(*args, **kwargs)
        
class LunchBooking(models.Model):
    quantity = models.PositiveIntegerField()
    day = models.DateField()
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)
    type = models.ForeignKey(
        Lunch,
        on_delete=models.CASCADE,
        blank = True,
        )
    booking = models.ForeignKey(
        Booking,
        related_name='booked_lunches',
        on_delete=models.CASCADE,
        )

    class Meta:
        verbose_name = 'lunchbokning'
        verbose_name_plural = 'lunchbokningar'
        
    def __str__(self):
        return '%s, %s' % (self.quantity, self.type)

    def save(self, *args, **kwargs):
        self.subtotal = self.type.price * self.quantity
        super(LunchBooking, self).save(*args, **kwargs)
        
class PackageBooking(models.Model):
    pass



'''
Models and Managers for availabilies of items to be booked.

Bikes, Rooms, ...
'''
# Availability manager
def perdelta(start, end, delta):
    curr = start
    while curr <= end:
        yield curr
        curr += delta
        
def find_index(lst, thing):
    for sublist, bike_no in enumerate(lst):
        try:           
            bike_ind = bike_no.index(thing)
        except ValueError:
            continue
        return sublist, bike_ind

# Abstract model for availability
class Available(models.Model):
    available_date = models.DateField()
    available = models.BooleanField(default=True)
    
    class Meta:
        abstract = True        
        
                    
class BikeAvailableManager(models.Manager):
    '''
    Manager for the available bikes. Takes care of booking/unbooking of bikes,
    has getter functions for bikes on specific dates and can create new and destroy
    old availabilities for bikes. 
    
    MOST FUNCTIONS NEED TESTING!!!
    '''
        
    def create_available_bike(self, bike, date):
        available_bike = self.create(bike=bike, available_date=date)
        return available_bike
    
    def destroy_available_bike(self, bike, date):
        self.get(bike=bike, available_date=date).delete()
    
    def bike_available_for_date(self, bike, date):
        """
        Method that takes one bike and one date and returns the
        BikeAvailable.available for that date, and a quality flag
        that the bike is possible to book that day.
        
        Used in:
        Bike.book.get_available()
        """
        success = False
        avbl = False
        try:
            bk = self.get(bike=bike, available_date=date)
            avbl = bk.available
            success = True
            return avbl, success
        except:
            return avbl, success
            
    def bike_for_dates(self, bike, dates):
        '''
        Method that takes one bike and a list of dates as arguments. 
        Returns true if the bike is available for all dates, otherwise returns
        false.
        '''
        for date in dates:
            try:
                self.get(bike=bike, available_date=date, available=True)
            except:
                return False
            
        return True
    
    def get_available_bikes_for_dates(self, attr, amount, start_date, end_date, duration=None):
        '''
        Method that builds a list of the first bikes of a given attribute that
        are available for all dates from start_date to end_date. Returns True 
        and the list of available bike objects. If not sufficiently many bikes
        are found the method returns False and the list of bikes that were found.
        
        Used in:
        BikeBookingResponse(APIView).post
        
        '''
        if not duration:
            duration = end_date - start_date
        
        date_list = create_date_list(start_date, duration.days)
        available_bike_list =[]
        bikes = Bike.objects.filter(attribute=attr)
        # Check in order if the bikes are available during the dates
        for bike in bikes:
            available = self.bike_for_dates(bike, date_list)    
            # If the bike is available, add it to the bike list.
            if available:
                available_bike_list.append(bike)
                    
            if len(available_bike_list) == amount:
                return True, available_bike_list
        return False, available_bike_list
            
    def get_all_bikes_for_day(self, day):
        '''
        Returns all bikes that are available for a given day
        
        Used in:
        calendar
        '''
        return super(BikeAvailableManager, self).get_queryset().filter(
            Q(available_date=day) & Q(available=True))
        
    def book_bike(self, booking, bike, date):
        '''
        Takes one bike object, a booking object and one date as arguments.
        Books the bike and saves it.
        
        Used in:
        BikesBooking.setBikes()
        '''
        try:
            # Try to find the right BikeAvailable object
            bk = BikeAvailable.objects.get(bike=bike, available_date=date)
        except ObjectDoesNotExist:
            # If it does not exist, return False
            return False
        bk.available = False
        bk.bookings = booking
        bk.save()
        return True
    
    def unbook_bike(self, bike, date):
        '''
        Takes one bike object and one date as arguments.
        Unbooks the bike and saves the changes.
        
        Used in:
        Bookingadmin.cancel
        '''
        bk = BikeAvailable.objects.get(bike=bike, available_date=date)
        print(bk)
        bk.available = True
        bk.bookings = None
        bk.save()
        print(bk.available, bk.bookings)
                       
# Availability for bikes
class BikeAvailable(Available):
    bike = models.ForeignKey(
        Bike,
        related_name='availability',
        on_delete=models.PROTECT,
        blank = True
        )
    
    bookings = models.ForeignKey(
        BikesBooking,
        related_name='availableBike',
        on_delete=models.PROTECT,
        blank = True,
        null = True
        )
    
    objects = BikeAvailableManager()  # Extended manager for finding dates
    
    class Meta:
        verbose_name = 'tillgänglighet cykel'
        verbose_name_plural = 'tillgänglighet cyklar'
        index_together = ['bike', 'available_date']
        ordering = ['available_date', 'bike', 'available']
        
    def __str__(self):
        return str(self.bike)
    

  
# Rooms
# Not needed until we can search external databases
class RoomsAvailable(Available):
    room = models.ForeignKey(
        Rooms,
        on_delete=models.PROTECT,
        null = True
        )
    bookings = models.ForeignKey(
        RoomsBooking,
        related_name= 'available_rooms'
        )

###############################################################################

