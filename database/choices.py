'''
Created on 26 nov. 2016

@author: Adrian
'''
from datetime import date, datetime, timedelta
Lunch_Choices = [
    ('vegetarian', 'vegetarisk'),
    ('meat', 'kallskuret'),
    ('fish', 'Vätternröding'),
    ]

Bike_Extra_Choices =[
    ('child_seat', 'barnsadel'),
    ('bike_carriage', 'cykelkärra'),
        ]

Bike_Attribute_Choices = [
    ('adult', 'vuxen'),
    ('young', 'ungdom'),
    ('child', 'barn'),
    ('smallChild', 'småbarn'),
    ]

Bike_Wheelsize_Choices = [
    ('large', '28"'),
    ('medium', '26"'),
    ('small', '22"'),
    ]

Room_Standard_Choices = [
    ('hotel', 'Hotell'),
    ('hote_budget', 'Hotell budget'),
    ('hostel', 'Vandrarhem'),
    ]

Booking_choices = [
    ('B', 'Cykel'),
    ('A', 'Boende'),
    ('L', 'Lunch'),
    ('P', 'Paket'),
    ('E', 'Event')
    ]

Brand_choices = [
    ('LB', 'LunchBots'),
    ('CC', 'Clean Canteen'),
    ]

Action_Choices = [
    ('create', 'skapa tillgänglighet'),
    ('delete', 'ta bort tillgänglighet'),
    # ('update', 'uppdatera en tillgänglighet'),
    ]

Discount_Code_Choices =[
    ('amount', 'Fast summa'),
    ('percentage', 'Procent'),
    ('offer', 'Erbjudande'),
    ('gift', 'Presentkort')
    ] 

now = datetime.now().year
YEARS = {
    now: str(now),
    now + 1: str(now + 1),
    now - 1: str(now - 1),
    }

MONTHS = {
    1: 'Januari', 5: 'Maj', 6: 'Juni', 7:'Juli', 8: 'Augusti',
    9: 'September', 10: 'Oktober'
    }

Day_Choices = [
    (timedelta(days=1), '1 Dag'),
    (timedelta(days=2), '2 Dagar'),
    (timedelta(days=3), '3 Dagar'),
    (timedelta(days=4), '4 Dagar'),
    (timedelta(days=5), '5 Dagar'),
    (timedelta(days=6), '6 Dagar'),
    (timedelta(days=7), '7 Dagar'),
    ]

booking_status_codes = [
    ('Cancelled', 'Avbokad'),
    ('Active', 'Aktiv'),
    ('completed', 'Genomförd'),
    ('preliminary', 'Preliminär')
    ]
