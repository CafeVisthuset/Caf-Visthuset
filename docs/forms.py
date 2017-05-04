'''
Created on 1 maj 2017

@author: adrian
'''
from django import forms
from .models import EmailTexts

class EmailTextForm(forms.ModelForm):
    
    class Meta:
        model = EmailTexts
        fields = ['name', 'short_description', 'title', 'plain_text', 'html_message']
        
        help_texts = {
            'plain_text': '''Ren text, ska vara detsamma som html_texten. Kan innehålla Django template-taggar, men inte HTML. 
            Båda behövs för att alla ska kunna öppna meddelandet oavsett epost-klient.''',
            'html_message': 'HTML-version av den rena texten. Denna används sedan för att berätta för Django hur mejlet ska byggas ihop.',
            'short_description': 'En kort förklaring kring meddelandet, till exempel vart det används och när.',
            'name': 'Unikt namn på meddelande-mallen, används för att hämta mallen men syns inte utåt',
            'title': 'E-postmeddelandets ämne',
            }
        labels = {
            'name': 'Namn',
            'short_description': 'Kort förklaring',
            'created': 'Skapat',
            'updated': 'Uppdaterat',
            'title': 'Ämne',
            'plain_text': 'Meddelande som ren text',
            'html_message': 'Meddelande som HTML',
            }