from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage

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
# register page
admin.site.unregister(FlatPage)    
admin.site.register(FlatPage, FlatPageAdmin)