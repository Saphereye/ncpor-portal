from django.contrib import admin
from django.urls import path, include
from . import views
from django.shortcuts import render, redirect

app_name = 'extras'

urlpatterns = [
    path('', views.home),
    path('credits', views.credits),
]