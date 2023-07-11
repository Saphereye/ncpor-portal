from django.contrib import admin
from .models import RequestToReview

@admin.register(RequestToReview)
class CoordinatorRequestToReviewAdmin(admin.ModelAdmin):
    list_display = [field.name for field in RequestToReview._meta.get_fields() if field.concrete]