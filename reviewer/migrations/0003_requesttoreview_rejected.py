# Generated by Django 4.2.3 on 2023-07-12 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviewer', '0002_requesttoreview_accepted'),
    ]

    operations = [
        migrations.AddField(
            model_name='requesttoreview',
            name='rejected',
            field=models.BooleanField(default=False),
        ),
    ]
