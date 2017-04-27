from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=100)
    description = RichTextField(max_length=500)
    text = RichTextField(max_length=2000)
    image = models.ImageField(upload_to='static/img/uploads/')
    #image = models.ImageField(upload_to=os.path.join(os.path.abspath(''), 'static/img/uploads/'))
    imageAlt = models.CharField(max_length=30, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    pub_start = models.DateField()
    pub_end = models.DateField()
    published = models.BooleanField(default=False)
        
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Evenemang'
        ordering = ('-published', )