from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'authentication'

urlpatterns = [
    path('', views.welcome),
    path('choose_division', views.division_choose),
    path('register', views.register),
    path('details', views.details),
]