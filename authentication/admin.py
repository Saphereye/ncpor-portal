from django.contrib import admin
from .models import CustomUser, Details

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "is_staff", "is_superuser", "is_active", "last_login", "date_joined")  # Customize the displayed fields
    list_filter = ("is_staff", "is_superuser", "is_active")

@admin.register(Details)
class DetailsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Details._meta.get_fields() if field.concrete]  # Customize the displayed fields
    # list_filter = ('age',)
