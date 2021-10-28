from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('results/<int:pk_order>/', views.results, name='result'),
]
