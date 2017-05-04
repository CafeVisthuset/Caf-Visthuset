from django.core.exceptions import ValidationError

def ValidateAnomaly(self):
    if self.anomaly and (self.measure == None or self.measure == ''):
        raise ValidationError('Du har fylllt i en avvvikelse, men ingen åtgärd.'
        )
