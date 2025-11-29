from django.urls import path
from . import views

urlpatterns = [
    path('', views.covid_numbers, name='covid_numbers')
]
