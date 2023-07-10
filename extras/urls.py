from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'extras'

urlpatterns = [
    path('credits', views.credits),
]