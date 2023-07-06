from django.db import models

class Revisers(models.Model):
    reviser_email = models.EmailField()
    proposal_number = models.CharField(max_length=12)
