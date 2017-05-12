'''
Created on 13 jan. 2017

@author: adrian
'''
from calendar import HTMLCalendar, monthrange
from database.models import BikeAvailable
from Economy.models import Event
from django import template
from datetime import date, datetime
from itertools import groupby

from django.utils.html import conditional_escape as esc
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from database.helperfunctions import named_month

register = template.Library()

def do_event_calendar(parser, token):
    """
    The template tag's syntax is {% reading_calendar year month reading_list %}
    """
    
    try:
        tag_name, year, month, event_list = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires three arguments" % token.contents.split()[0])
    return EventCalendarNode(year, month, event_list)

class EventCalendarNode(template.Node):
    """
    Process a particaular node in the template. Fail silently.
    """
    
    def __init__(self, year, month, event_list):
        try:
            self.year = template.Variable(year)
            self.month = template.Variable(month)
            self.event_list = template.Variable(event_list)
        except ValueError:
            raise template.TemplateSyntaxError
    
    def render(self, context):
        try:
            # Get the variables from the context so the method is thread-safe
            my_event_list = self.event_list.resolve(context)
            my_year = self.year.resolve(context)
            my_month = self.month.resolve(context)
            cal = EventCalendar(my_event_list)
            return cal.formatmonth(int(my_year), int(my_month))
        except ValueError:
            return
        except template.VariableDoesNotExist:
            return
        
        
class EventCalendar(HTMLCalendar):
    """
    Override Python's calendar.HTMLCalendar to add the appropriate reading events to
    each day's table cell.
    """
    def __init__(self, events):
        super(EventCalendar, self).__init__()
        self.events = self.group_events_by_day(events)
        
    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += '  today'
            if day in self.events[day]:
                cssclass += '  filled'
                body = ['<ul>']
                for event in self.events[day]:
                    body.append('<li>')
                    body.append('<a href="%s">' % event.get_absolute_url())
                    body.append(esc(event.series.primary_name))
                    body.append('</a></li>')
                body.append('</ul>')
                return self.day_cell(cssclass, '<span class="dayNumber">%d</span> %s'
                                 % (day, ''.join(body)))
            return self.day_cell(cssclass, '<span class="dayNumberNoReadings">%d</span>' % (day))
        return self.day_cell('noday', '&nbsp;')
 
    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(EventCalendar, self).formatmonth(year, month)
    
    def group_events_by_day(self, events):
        field = lambda event: event.date_and_time.day
        return dict(
            [(day, list(items)) for day, items in groupby(events, field)]
            )
        
    def day_cell(self, cssclass, body):
        return'<td class="%s">%s</td>' % (cssclass, body)   
    
    
def this_month(request):
    """
    Show calendar readings this month
    """
    today = datetime.now()
    return calendar(request, today.year, today.month)

def calendar(request, year, month, series_id=None):
    """
    Show calendar of readings for a given month of a given year.
    ''series_id''
    The reading series to show. None shows all reading series.
    """
    
    my_year = int(year)
    my_month = int(month)
    my_calendar_from_month = datetime(my_year, my_month, 1)
    my_calendar_to_month = datetime(my_year, my_month, monthrange(my_year, my_month)[1])
    
    my_events = (Event.objects
                .filter(date_and_time__gte=my_calendar_from_month)
                .filter(date_and_time__lte=my_calendar_to_month))
    
    if series_id:
        my_events = my_events.filter(series=series_id)
        
    # Calculate values for the calendar controls. 1-indexed (Jan = 1)
    my_previous_year = my_year
    my_previuos_month = my_month - 1
    
    if my_previuos_month == 0:
        my_previous_year = my_year - 1
        my_previous_month = 12
    
    my_next_year = my_year
    my_next_month = my_month + 1
    if my_next_month == 13:
        my_next_year = my_year + 1
        my_next_month = 1
    
    my_year_after_this = my_year + 1
    my_year_before_this = my_year - 1
    return render_to_response("bookings/cal_template.html", {'readings_list': my_events,
                                                    'month': my_month,
                                                    'year': my_year,
                                                    'previous_month': my_previous_month,
                                                    'previous_month_name': named_month(my_previous_month),
                                                    'previous_year': my_previous_year,
                                                    'next_month': my_next_month,
                                                    'next_month_name': named_month(my_next_month),
                                                    'next_year': my_next_year,
                                                    'year_before_this': my_year_before_this,
                                                    'year_after_this': my_year_after_this,
                                                    
                                                    }, context_instance = RequestContext(request))
 
'''       
https://uggedal.com/journal/creating-a-flexible-monthly-calendar-in-django/
https://williambert.online/2011/06/django-event-calendar-for-a-django-beginner/
'''        

class BikeCalendar(HTMLCalendar):
    
    def __init__(self, bikes):
        super(BikeCalendar, self).__init__()
        self.bikes = self.group_bikes_by_day(bikes)
        
    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if day == date.today():
                cssclass += ' today'
            if day in self.bikes:
                cssclass += ' filled'
                body = ['<ul>']
                body.append('{} cyklar lediga'.format(len(self.bikes[day])))
                #for bike in self.bikes[day]:
                #    body.append('<li>')
                #    body.append(str(bike))
                #    body.append('</li>')
                body.append('</ul>')
                return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')
    
    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(BikeCalendar, self).formatmonth(year, month)
    
    def group_bikes_by_day(self, bikes):
        field = lambda bike: bike.available_date.day
        return dict(
            [(day, list(items)) for day, items in groupby(bikes, field)])
        
    def day_cell(self, cssclass, body):
        return'<td class="%s">%s</td>' % (cssclass, body)    