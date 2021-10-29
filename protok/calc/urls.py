from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contacts', views.contacts, name='contacts'),
    path('results/<int:pk_order>/', views.results, name='result'),
]
