from django.forms import ModelForm
from .models import Transformer, HighVoltageDevice


class TransformerForm(ModelForm):
    class Meta:
        model = Transformer
        fields = ['transformer_type', 'connection_scheme', 'power']


class HighVoltageDeviceForm(ModelForm):
    class Meta:
        model = HighVoltageDevice
        fields = ['input_type', 'voltage', 'arrester', 'equipment_type',
                  'registration', 'connection_type', 'documentation']
