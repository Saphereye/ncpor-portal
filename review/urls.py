from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'review'

urlpatterns = [
    path('', views.revision),
    path('<slug:proposal_number>/', views.revision),
    path('agree/<slug:proposal_number>/', views.agree),
    path('decline/<slug:proposal_number>/', views.decline),
]

