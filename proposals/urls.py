from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'proposals'

urlpatterns = [
    path('home', views.home),
    path('submit', views.submit),
    path('submit/details', views.submit_details),
    path('submit/details/<slug:title>/', views.submit_details),
    path('submit/files', views.submit_files),
    path('submit/files/<slug:title>/', views.submit_files),
    path('submit/summary', views.submit_summary),
    path('submit/summary/<slug:title>/', views.submit_summary),
    path('submit/finish', views.submit_finish),
    path('incomplete', views.incomplete_proposals)
]

