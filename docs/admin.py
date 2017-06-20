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
    list_display = ['name', 'created', 'updated', 'title']

class PageContentInline(admin.StackedInline):
    model = PageContent
    fieldsets = [
        ('Stycke',              {'fields': ['shortname', 'page', 'order', 'created', 'updated']}),
        ('Text',            {'fields': ['headline', 'text', 'image', 'image_alt']}),
        ('Publicera?',      {'fields': ['publish']}),
        ]
    readonly_fields = ['created', 'updated']
    extra = 1
    
    class Media:
        css = {
            'all': ('/static/css/admin/inlines.css'),
            }
        
class PageBannerInline(admin.StackedInline):
    model = Banner
    fieldsets = [
        ('Sidhantering',        {'fields': ['page', 'carousel', 'order'],
                                 'description': """Här hanteras vilken sida som ska använda bannern.
                                 Om Karusell är ikryssad så kommer bilden att finnas med i karusellen, annars finns
                                 den som en statisk bild ovanför den enskilda sidan."""}),
        ('Texter',              {'fields': ['h1', 'h3']}),
        ('Bilder',              {'fields': ['image']}),
        ]
    max_num = 1
    
@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,          {'fields': ['name', 'code', 'static_banner', 'created', 'updated']}),
        ('Texter',      {'fields': ['title', 'headline', 'ingress']}),
        ]
    readonly_fields = ['created', 'updated']
    list_display = ['name', 'title', 'created', 'updated']
    inlines = [PageBannerInline, PageContentInline, ]
    
@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    '''
    Admin to handle carousel banners specifically. Page specific banners are handled in
    PageAdmin.
    '''
    fieldsets = [
        ('Sidhantering',        {'fields': ['internal', 'page', 'carousel', 'order', 'publish'],
                                 'description': """Här hanteras vilken sida som ska använda bannern.
                                 Om Karusell är ikryssad så kommer bilden att finnas med i karusellen, annars finns
                                 den som en statisk bild ovanför den enskilda sidan."""}),
        ('Texter',              {'fields': ['h1', 'h3']}),
        ('Bilder',              {'fields': ['image']}),
        ]
    list_display=['internal', 'page', 'carousel', 'order', 'publish']
# register page
admin.site.unregister(FlatPage)    
admin.site.register(FlatPage, FlatPageAdmin)