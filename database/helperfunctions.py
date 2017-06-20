'''
Created on 1 jan. 2017

@author: Adrian
'''
from datetime import datetime, date, timedelta


# For summing up e.g., the price in a booking
def listSum(NumberList):
    '''
    Adds numbers in a list.
    '''
    total = 0
    for number in NumberList:
        total += number
        
    return total

def named_month(month_number):
    """
    Return the name of the month, given the number.
    """
    return date(1900, month_number, 1).strftime("%B")

def create_date_list(start_date, duration):
    '''
    Creates a list of datetime days from start_date, to end_date
    '''
    return [start_date + timedelta(days=x) for x in range(0, duration)]

def date_list_in_bike_list(date_lst, bike_lst):
    '''
    Takes a list of dates and a list of available bikes. If all the dates in the
    date list is also in the bike list, the function returns true
    '''
    
    lst = []
    for element in date_lst:
        if element in bike_lst:
            lst.append(element)
            if lst == date_lst:
                return True
    return False
    
def choicegen(start, end):
    '''
    returns a list with key,value tuples to be used in form choices. 
    '''
    return [(number, '%s' % (number)) for number in range(start, end+1)]
    