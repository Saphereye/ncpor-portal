from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'reviewer'

urlpatterns = [
    path('pending/', views.pending),
    path('pending/<slug:proposal_number>/', views.pending),
    path('agree/', views.agree),
    path('agree/<slug:proposal_number>/', views.agree),
    path('decline/', views.decline),
    path('decline/<slug:proposal_number>/', views.decline),
]