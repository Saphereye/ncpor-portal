from django.contrib import admin
from .models import Revisers

@admin.register(Revisers)
class RevisersAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Revisers._meta.get_fields() if field.concrete]