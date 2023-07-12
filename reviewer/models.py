from django.db import models

# Create your models here.
class RequestToReview(models.Model):
    email = models.EmailField()
    proposal_number = models.CharField(max_length=12)
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    
    