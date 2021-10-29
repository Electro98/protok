from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contacts/', views.contacts, name='contacts'),
    path('get_contact/', views.get_contact, name='get_contact'),
    path('results/<int:pk_order>/', views.results, name='result'),
]
