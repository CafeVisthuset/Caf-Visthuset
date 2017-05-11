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
        
class Page(models.Model):
    '''
    Model for each page to be used in the CMS. Right now it is used as a
    foreign key to the page Texts. This is made so that the Admin page can
    have choices on which page the text should appear.
    
    To find the right texts to return to the template, use:
    PageTexts.objects.filter(page__name = <page>)
    
    So far <page> is hardcoded in the view, but could later be done more dynamic.
    
    These models are used for ease of updating texts without having to commit to
    git and update hard code on the server.
    
    Future adds could be f.ex.
    # Template_name
    # Template renderer / create template
    # Url-field and what is needed to render a template
    '''
    name = models.SlugField(help_text='identifying slug for page, e.g., "meny"')
    title = models.CharField(max_length=100, help_text='sidans titel')
    headline = models.CharField(max_length=100, help_text='H1-rubrik')
    ingress = RichTextField(max_length=500, help_text='kort ingress, max 500 tecken')
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'sida'
        verbose_name_plural = 'sidor'
        
        
class PageContent(models.Model):
    '''
    Model used for rendering and quering content to templates in simple CMS. 
    '''
    shortname = models.CharField(max_length=30, help_text='ex. kaffe')
    page = models.ForeignKey(
        Page,
        on_delete=models.PROTECT,
        blank = True,
        help_text = 'På vilken sida vill du publicera detta?'
        )
    headline = models.CharField(blank=True, max_length=100, help_text='kort H2-rubrik, ex "riktigt gott kaffe"')
    text = models.TextField(max_length = 2000)
    order = models.IntegerField(choices=[(1, 1),(2, 2),(3, 3),(4,4)], help_text='1 är innehåll högt upp på sidan, 4 långt ner')
    image = models.ImageField(upload_to='/static/img/uploads/', blank=True)
    image_alt = models.CharField(max_length=50, blank=True)
    publish = models.BooleanField(default=False)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return '{}, {}'.format(self.page, self.shortname)
    
    class Meta:
        verbose_name = 'sidinnehåll'
        verbose_name_plural = 'sidinnehåll'
        ordering = ['-publish', 'page', 'shortname']
        