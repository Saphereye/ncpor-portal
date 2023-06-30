from django.db import models

class Details(models.Model):
    DISCIPLINE_CHOICES = (
            ('A', 'Atmospheric Science'),
            ('O', 'Oceanography'),
            ('G', 'Geology and Palosciences'),
            ('R', 'Glaciology and Remote Sensing'),
            ('E', 'Environmental Science'),
            ('B', 'Biology'),
            ('T', 'Other'),
        )
    FRESHNESS_CHOICE = (
        ('O', 'Ongoing'),
        ('N', 'New')
    )
    title_of_proposal = models.CharField(max_length=20, null=False)
    major_discipline = models.CharField(max_length = 1,choices = DISCIPLINE_CHOICES, null=False)
    sub_theme = models.CharField(max_length=20, null=False)
    key_words = models.CharField(max_length=50)
    freshness = models.CharField(max_length = 1,choices = FRESHNESS_CHOICE, null=False, name="Ongoing/New")
    brief_description = models.TextField(max_length=250)
