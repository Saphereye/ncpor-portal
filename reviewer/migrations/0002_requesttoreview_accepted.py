# Generated by Django 4.2.3 on 2023-07-11 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviewer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='requesttoreview',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
    ]
