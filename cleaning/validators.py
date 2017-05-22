from django.core.exceptions import ValidationError

def ValidateAnomaly(self):
    if self.anomaly and (self.measure == None or self.measure == ''):
        raise ValidationError('Du har fylllt i en avvvikelse, men ingen åtgärd.'
        )

def validateTemperatureAnomaly(self):
    # Validate that the measure is filled in if there is a temperature
    # anomaly
    if self.anomaly and not self.measure:
        raise ValidationError(
                'Du har fyllt i en avvikelse utan att fylla i en åtgärd.')