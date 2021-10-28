from django.shortcuts import render
from .forms import TransformerForm, HighVoltageDeviceForm, ClientForm


def index(request):
    forms = []
    forms.append(TransformerForm())
    forms.append(HighVoltageDeviceForm())
    return render(request, 'calc/form.html', {'forms': forms})


def getcontacts(request):
    form = ClientForm()
    return render(request, 'calc/contacts.html', {'form': form})
