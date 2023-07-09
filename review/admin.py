from django.contrib import admin
from .models import Revisers, Review

@admin.register(Revisers)
class RevisersAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Revisers._meta.get_fields() if field.concrete]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Review._meta.get_fields() if field.concrete]