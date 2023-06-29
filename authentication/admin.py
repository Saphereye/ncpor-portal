from django.contrib import admin
from .models import CustomUser, Details

admin.site.register(CustomUser)
# admin.site.register(Details)

@admin.register(Details)
class DetailsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Details._meta.get_fields() if field.concrete]  # Customize the displayed fields
    # list_filter = ('age',)
