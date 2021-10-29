from django.shortcuts import render, get_object_or_404, redirect
from .forms import TransformerForm, HighVoltageDeviceForm, ClientForm, OrderForm
from django.core.mail import send_mail, EmailMessage, get_connection
from .models import Order


def setname(obj, name):
    obj.name = name
    return obj

def index(request):
    forms = []
    forms.append(setname(TransformerForm(), 'Трансформатор'))
    forms[0].fields['power'].min_value = 20
    forms[0].fields['power'].max_value = 630
    forms.append(setname(HighVoltageDeviceForm(), 'ВН'))
    forms[1].fields['voltage'].max_value = 10000
    return render(request, 'calc/form.html', {'forms': forms, 'display_element': forms})


def get_contact(request):
    return redirect(f'result/{None}/', permanent=True)


def contacts(request):
    form = ClientForm()
    order = OrderForm()
    return render(request, 'calc/contacts.html', {'form': form, 'order': order})


def results(request, pk_order):
    order = get_object_or_404(Order, pk=pk_order)
    return render(request, 'calc/results.html', {'order': order, 'client': order.client})


def send_email(order_id):
    order = Order.objects.get(pk=order_id)
    # email.attach([order.path for order in order.documentation_assembling()])
    with get_connection() as connection:
        email = EmailMessage(  # C8.fnjAnL7iAACw
            'Hello',
            'From your mom gay',
            "a4dmindjango@yandex.ru",
            [order.client.email],
            [],
            connection=connection
        )
        print(f'Почта ={order.client.email}')
        email.send()
