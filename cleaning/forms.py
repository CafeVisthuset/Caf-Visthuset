'''
Created on 9 nov. 2016

@author: Adrian
'''
from django import forms
from cleaning.models import *

# Special Choice Fields for models
class ColdStorageChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return"%s, %s"%(obj.type, obj.location)
      
class RoutineForm(forms.ModelForm):
    class Meta:
        model = Routine
        fields = ['name', 'purpose', 'description', 'monitoring', 'anomaly_measure', 'anomaly_correction']
        labels = {'name': 'Namn',
                  'purpose': 'Rutinens syfte',
                  'description': 'Beskrivning',
                  'monitoring': 'Övervakning',
                  'anomaly_measure': 'Åtgärd vid avvikelse',
                  'anomaly_correction': 'Korrigering vid avvikelse',
                  'created': 'Skapad',
                  'updated': 'Uppdaterad'}
        
        help_texts = {'description': 'Här beskrivs hur rutinen går till, gärna i punktform',
                      'monitoring': 'Hur och hur ofta kollar vi att rutinen utförs?',
                      'anomaly_measure': 'Vilken åtgärd vidtar vi om någonting brister?',
                      'anomaly_correction': '''Hur korrigerar vi en brist som uppstår? 
                      Måste till exempel en vara kasseras?'''}
        
class HazardForm(forms.ModelForm):
    class Meta:
        model = Hazard
        fields = ['name', 'type', 'how', 'description', 'analysis']
        labels = {'name': 'Fara',
                  'created': 'Skapad',
                  'updated': 'Uppdaterad',
                  'type': 'Från',
                  'how': 'Hur',
                  'description': 'Beskrivning',
                  'analysis': 'Analys',
                  }
        help_texts ={'type':'Vad är det för typ av fara? Vartifrån kommer den?',
                    'how': '''Hur uppkommer faran? 
                    Förekomst: Finns risk för fara enbart genom att något förekommer i köket?
                    Tillförsel: Finns risk att vi tillför något farligt?
                    Tillväxt: Är det risk ifall något, till exempel en bakterie tillväxer?
                    Överlevnad: Finns risk att en bakteria överlever till exempel en temperaturbehandling?''',
                    'description': '''Beskriv faran, varför är den farlig och vad är till exempel
                    besvären för en gäst om något går fel? ''',
                    'analysis': '''Gör en analys av faran, hur allvarlig är den? Är våra grundförutsättningar och
                    rutiner tillräckliga för att minimera eller elimiminera faran?''',
                    }

class ControlPointForm(forms.ModelForm):
    class Meta:
        model = ControlPoint
        fields = ['routine', ]
        labels = {
            'routine_sufficient': 'Är rutinen tillräcklig?',
            'routine': 'Rutin',
            }
        help_texts = {
            'routine_sufficient': '''Räcker rutinerna för att eliminera faran? Om inte skapas en kritisk
                    kontrollpunkt där extra övervakning och tillåtna gränser anges''',
            }