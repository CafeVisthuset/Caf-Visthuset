from django.contrib import admin
from .models import Event

# Register your models here.
admin.site.register(Event)
class EventsAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['title', 'describtion', 'text']}),
        ('Bilder',          {'fields': ['image', 'imageAlt']}),
        ('Publicering',     {'fields': ['published', 'pub_start', 'pub_end']}),
        ]
    
    list_display = ['title', 'start_date', 'end_date', 'pub_start', 'pub_end', 'published']
