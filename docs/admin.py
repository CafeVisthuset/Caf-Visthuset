from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from .forms import EmailTextForm

from .models import *

# Register your models here.
class FlatPageAdmin(FlatPageAdmin):
    fieldsets = (
        (None,  {'fields': ('url', 'title', 'content', 'sites')}),
        ('Advanced options', {
            'classes': ('collapse', ),
            'fields': (
                'enable_comments',
                'registration_required',
                'template_name',
                ),
            }),
        )
    
@admin.register(EmailTexts)
class EmailTextAdmin(admin.ModelAdmin):
    form = EmailTextForm
    fieldsets = [
        (None,      {'fields': ['name', 'short_description', 'created', 'updated']}),
        ('Epost-meddelandet',   {'fields': ['title', 'plain_text', 'html_message', 'image']})
        ]
    readonly_fields = ['created', 'updated']
    list_fields = ['name', 'created', 'updated', 'title']

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,          {'fields': ['name', 'created', 'updated']}),
        ('Texter',      {'fields': ['title', 'headline', 'ingress']}),
        ]
    readonly_fields = ['created', 'updated']
    list_fields = ['name', 'created', 'updated']

@admin.register(PageContent)
class PageContentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['shortname', 'page', 'order', 'created', 'updated']}),
        ('Text',            {'fields': ['headline', 'text', 'image', 'image_alt']}),
        ('Publicera?',      {'fields': ['publish']}),
        ]
    readonly_fields = ['created', 'updated']
    list_display = ['shortname', 'page', 'order', 'publish', 'created', 'updated']
    
# register page
admin.site.unregister(FlatPage)    
admin.site.register(FlatPage, FlatPageAdmin)