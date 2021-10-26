from django.shortcuts import render
from .forms import TransformerForm, HighVoltageDeviceForm


def index(request):
    forms = []
    forms.append(TransformerForm())
    forms.append(HighVoltageDeviceForm())
    return render(request, 'calc/form.html', {'forms': forms})
