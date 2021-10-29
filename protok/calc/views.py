from django.shortcuts import render, get_object_or_404, redirect
from .forms import TransformerForm, HighVoltageDeviceForm, ClientForm, OrderForm
from django.core.mail import send_mail, EmailMessage, get_connection
from django.views.decorators.csrf import csrf_protect
from .models import Order


def setname(obj, name):
    obj.name = name
    return obj

def index(request):
    forms = []
    forms.append(setname(TransformerForm(), 'Трансформатор'))
    forms.append(setname(HighVoltageDeviceForm(), 'ВН'))
    return render(request, 'calc/form.html', {'forms': forms, 'display_element': forms})


@csrf_protect
def get_contact(request):
    if request.method == 'POST':
        client = ClientForm(request.POST)
        order = OrderForm(request.POST, request.FILES)
        print(request.__dict__)
        if client.is_valid():
            print('Ohh')
        else:
            print(client.errors.as_data())
        if order.is_valid():
            print('Fuck')
        else:
            print(order.errors.as_data())
        if not client.is_valid() or not order.is_valid():
            return render(request, 'calc/contacts.html', {'client': client, 'order': order})
    return redirect(f'/result/{None}/', permanent=True)


def contacts(request):
    client = ClientForm()
    order = OrderForm()
    return render(request, 'calc/contacts.html', {'client': client, 'order': order})


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
