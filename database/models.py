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

'''
TODO:
* Gör klart alla modeller för att kunna genomföra bokningar
    # Grundläggande modeller som bara håller data (ex. cyklar el. utrustning) 
        görs abstrakta
        - Eventuellt: Skadorna är också en underklass av cyklar
    # Bokningsmodeller görs som förlängningar av de abstrakta modellerna
        - cykelbokningar
        - lunchbokningar
        - boendebokningar
        - tillbehörsbokningar (ex cykelkärra)
    # Gör det möjligt att ange om bokningar är preleminära
    # Gör det möjligt att föra statistik över sålda paket
    # Lägg in tillgänglighet för cyklar vissa datum
    
* Gör managers till bokningsmodellerna för att kunna göra sökningar
* Lägg in modeller för generiska bokningar/eventbokningar
* Lägg in funktion för att skapa bokningsnummer

'''

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
    
    def __str__(self):
        return "%scykel %s" % (self.attribute, self.number)
    
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
        print(kwargs['kwargs'])
        try:
            # first try to find by email
            guest = Guest.objects.get(email=email)
            print('success')
        except MultipleObjectsReturned:
            # specify the search
            print('tried to be more specific')
            guest = Guest.objects.get(first_name=first_name, last_name=last_name, email=email)
            
        except ObjectDoesNotExist:
            # If the object doees not exist, create a new one
            password = User.objects.make_random_password()
            print
            try:
                guest = Guest.objects.create(username=email, password=password, first_name=first_name,
                              last_name = last_name, email=email,
                              phone_number = kwargs['kwargs']['phone_number'],
                              newsletter = kwargs['kwargs']['newsletter'])
            except:
                print('last option')
                # if the username is already taken, create a unique username for the person
                # this hopefully works, otherwise it fails.
                username= '.'.join(['email', 'first_name', 'last_name'])
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
Boking models.

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
    
    Ex of procedure for creating a new bookng
    1. Initiate booking,
        Booking.book.create_booking(guest, start_date, end_date, 
                                    numberOfGuests, special request)
    
    2. Set attributes of booking, use the setter functions
        ex. Booking.book.setBikeBooking()
        
    3. Get attributes for booking to be returned to user (optional)
        ex. Booking.book.getBikeBooking(booking_number)
    
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
    # Setters
    :setBikeBooking
    :setBikeExtraBooking
    :setLunchBooking
    :setAccomodationBooking
     
    '''
    # Create, update, delete
    def create_booking(self, guest, start_date, end_date, numberOfGuests, special_requests):
        booking = self.create(guest=guest,
                              start_date=start_date, 
                              end_date=end_date,
                              numberOfGuests=numberOfGuests,
                              special_requests=special_requests)
        return booking
        
    def update_booking(self, booking_number, **kwargs):
        booking = self.get(booking=booking_number)
        return booking.update(**kwargs)
        
    def delete_booking(self, booking, status_code):
        '''
        Make booking inactive with status code.
        '''
        pass
    
    # Functions to update specific parts of bookings
    def check_in_booking(self, booking_number):
        '''
        Check in guest. NEED TESTING
        '''
        booking = self.get(booking=booking_number)
        return booking.update(checked_in=True)
    
    def check_out_booking(self, booking_number):
        '''
        Check out guest. NEED TESTING
        '''
        booking = self.get(booking=booking_number)
        return booking.update(checked_out=True)
    
    # Getters
    def getBookingStatus(self, booking_number):
        '''
        Returns the status of the booking as a tuple. NEEDS TESTING!!
        '''
        booking = self.get(booking=booking_number)
        return ('booking.status_code', 
                booking.checked_in,
                booking.checked_out,
                booking.payed)
        
    def getBikeBooking(self, booking_number):
        booking = self.get(booking=booking_number)
        return booking.booked_bike
    
    def getLunchBooking(self, booking_number):
        booking = self.get(booking=booking_number)
        return booking.booked_lunches
    
    '''
    SETTERS
    
    Use to create bookings of e.g., bikes underneath a booking.
    '''
    def setBikeBooking(self, type, amount, start_date, duration):
        booking_dates = create_date_list(start_date, duration)
        
        # check if there are enough available bikes for the dates
        available_bike_list = []
        for bike in Bike.objects.filter(attribute=type):
            # Check in order if the bikes are available during the dates
            available = BikeAvailable.objects.bike_for_dates(bike, booking_dates)
            
            # If the bike is available, add it to the bike list.
            if available:
                available_bike_list.append(bike)
                
            # If there are enough bikes
            if len(available_bike_list) == amount: 
                # Initiate bike booking
                bike_booking = self.booked_bike.create(start_date, end_date)
        
                bike_booking.set_bikes()
                '''
                
                '''
                return True, bike_booking
            
        return False, available_bike_list
    
    def setBikeExtraBooking(self, **kwargs):
        pass
    
    def setLunchBooking(self, **kwargs):
        pass
    
    def setAccomodationBooking(self, **kwargs):
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
    numberOfGuests = models.IntegerField(null= False, default = 2, verbose_name='antal gäster')
    special_requests = models.TextField(max_length = 255, null=True, blank= True, verbose_name= 'övrigt')
    
    # Fields for preliminary bookings
    preliminary = models.BooleanField(default=False, verbose_name='preliminär')
    longest_prel = models.DateTimeField(verbose_name='längsta preliminärbokning', null=True,
                                        validators= [validate_preliminary], blank=True)
   
    
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
        
        # create function that gathers all related bookings and calculates
        # the total price from their subtotals.
        
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
        on_delete=models.CASCADE,
        blank=True
        )
    booking = models.ForeignKey(
        Booking,
        related_name='booked_bike',
        on_delete=models.CASCADE,
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
        
        # Update Available bikes
        numdays = self.to_date.day - self.from_date.day
        date_list = [(self.from_date + timedelta(days=x)) for x in range(0,numdays + 1)]
            
        [BikeAvailable.objects.book_bike(
            bike=self.bike, date=date, booking=self) for date in date_list]
        
    '''
    TODO:
    # Lägg till __str__ för bike
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
    
    def bike_for_dates(bike, dates):
        '''
        Function that takes one bike and a list of dates as arguments. 
        Returns true if the bike is available during that day, otherwise returns
        false
        '''
        for date in dates:
            try:
                self.get(bike=bike, available_date=date, available=True)
            
            except:
                return False
            
        return True
                
    def get_bikes_for_day(self, day):
        return super(BikeAvailableManager, self).get_queryset().filter(
            Q(available_date=day) & Q(available=True))
        
    def book_bike(self, bike, booking, date):
        '''
        Takes one bike object, a booking object and one date as arguments.
        Books the bike and saves it.
        '''
        bk = self.get(bike=bike, available_date=date)
        bk.available = False
        bk.bookings = booking
        bk.save()
        
    def unbook_bike(self, bike, date):
        '''
        Takes one bike object and one date as arguments.
        Unbooks the bike and saves the changes.
        '''
        bk = self.get(bike=bike, available_date=date)
        bk.available = True
        bk.bookings = None
        bk.save()
                       
# Availability for bikes
class BikeAvailable(Available):
    bike = models.ForeignKey(
        Bike,
        on_delete=models.PROTECT,
        blank = True
        )
    
    bookings = models.ForeignKey(
        BikesBooking,
        related_name='availableBike',
        on_delete=models.CASCADE,
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

