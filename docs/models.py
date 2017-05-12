from django.db import models
from ckeditor.fields import RichTextField

#Only for development
import sys

class EmailTexts(models.Model):
    name = models.SlugField()
    short_description = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    plain_text = models.TextField(max_length=2000)
    html_message = RichTextField(max_length=2000)
    image = models.ImageField(upload_to='static/img/uploads/', blank=True, null=True)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name='epost-meddelande'
        verbose_name_plural = 'epost-meddelanden'