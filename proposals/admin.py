from django.contrib import admin
from .models import Details, Files, IncompleteProposals

@admin.register(Details)
class ProposalsDetailsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Details._meta.get_fields() if field.concrete]
    list_filter = ("major_discipline", "Ongoing/New")

@admin.register(Files)
class FilesAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Files._meta.get_fields() if field.concrete]

@admin.register(IncompleteProposals)
class IncompleteProposalsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in IncompleteProposals._meta.get_fields() if field.concrete]
