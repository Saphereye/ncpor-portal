from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'coordinator'

urlpatterns = [
   path('all', views.all),
   path('assign', views.assign),
   path('assign/<slug:proposal_number>', views.assign),
]