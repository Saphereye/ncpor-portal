# Generated by Django 4.2.2 on 2023-07-03 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0005_proposalmeta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='details',
            name='title_of_proposal',
            field=models.CharField(max_length=50, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='files',
            name='title_of_proposal',
            field=models.CharField(max_length=50, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='incompleteproposals',
            name='title',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='proposalmeta',
            name='title',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
