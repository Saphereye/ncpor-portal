from django.db import models
from authentication.models import CustomUser

class Details(models.Model):
    DISCIPLINE_CHOICES = (
            ('Atmospheric Science', 'Atmospheric Science'),
            ('Oceanography', 'Oceanography'),
            ('Geology and Palosciences', 'Geology and Palosciences'),
            ('Glaciology and Remote Sensing', 'Glaciology and Remote Sensing'),
            ('Environmental Science', 'Environmental Science'),
            ('Biology', 'Biology'),
            ('Other', 'Other'),
        )
    FRESHNESS_CHOICE = (
        ('Ongoing', 'Ongoing'),
        ('New', 'New')
    )
    email = models.EmailField()
    title_of_proposal = models.CharField(max_length=50, null=False , unique=True, primary_key=True)
    major_discipline = models.CharField(max_length = 30,choices = DISCIPLINE_CHOICES, null=False)
    sub_theme = models.CharField(max_length=20, null=False)
    key_words = models.CharField(max_length=50)
    freshness = models.CharField(max_length = 10,choices = FRESHNESS_CHOICE, null=False, name="Ongoing/New")
    brief_description = models.TextField(max_length=250)

class Files(models.Model):
    email = models.EmailField()
    title_of_proposal = models.CharField(max_length=50, null=False , unique=True, primary_key=True)
    cover_letter = models.FileField(null=True, blank=True, name="Attach Cover Letter", upload_to="media/")
    project_proposal = models.FileField(null=True, blank=True, name="Attach the detailed Project proposal(Download Template (.docx file) ", upload_to="media/")
    endorsement_letter = models.FileField(null=True, blank=True, name="Attach the detailed Project proposal(Download Appendix I Template (.docx file)", upload_to="media/")
    appendix_2 = models.FileField(null=True, blank=True, name="Attach Appendix II (Assessment for Ongoing project) Download Template for Appendix II", upload_to="media/")
    appendix_3 = models.FileField(null=True, blank=True, name="Attach Appendix III (Metadata format for Ongoing project)* Download Template for Appendix III", upload_to="media/")

class IncompleteProposals(models.Model):
    email = models.EmailField()
    title = models.CharField(max_length=50, null=False , unique=True)

class ProposalMeta(models.Model):
    email = models.EmailField()
    title = models.CharField(max_length=50, null=False , unique=True)
    is_author_approved = models.BooleanField(default=False)
    is_processed = models.BooleanField(default=False)