from django.forms import ModelForm
from .models import Transformer, HighVoltageDevice, Client, Order


class TransformerForm(ModelForm):
    class Meta:
        model = Transformer
        fields = ['transformer_type', 'connection_scheme', 'power']


class HighVoltageDeviceForm(ModelForm):
    class Meta:
        model = HighVoltageDevice
        fields = ['input_type', 'voltage', 'arrester', 'equipment_type',
                  'registration', 'connection_type']


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['full_name', 'organization', 'email', 'phone_number']


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['comment', 'documentation']
