# Generated by Django 4.2.2 on 2023-07-01 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='incompleteproposals',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='incompleteproposals',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
