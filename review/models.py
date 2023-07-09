from django.db import models

class Revisers(models.Model):
    reviser_email = models.EmailField()
    proposal_number = models.CharField(max_length=12)

class Review(models.Model):
    title = models.CharField(max_length=50)
    # No need for user to fill this
    major_discipline = models.CharField(max_length=50)
    pi_name = models.CharField(max_length=50)
    pi_institute = models.CharField(max_length=50)
    co_pi_name = models.CharField(max_length=50)
    co_pi_institute = models.CharField(max_length=50)

    # User need to fill these though
    recommendation = models.CharField(max_length=17, choices=(
        ("N", "No Recommendation"),
        ("A", "Accept"),
        ("M", "Major Revision"),
        ("m", "Minor Revision"),
        ("R", "Reject"),
    ))
    reviewer_comment = models.TextField() 
    reviewer_confidential_comment = models.TextField()
    overall_ranking = models.IntegerField(choices=(
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
            ('6', '6'),
            ('7', '7'),
            ('8', '8'),
            ('9', '9'),
            ('10', '10'),
            ))
