# Generated by Django 4.2.2 on 2023-07-01 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0002_incompleteproposals_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='Attach Appendix II (Assessment for Ongoing project) Download Template for Appendix II',
            field=models.FileField(blank=True, null=True, upload_to='media/'),
        ),
        migrations.AlterField(
            model_name='files',
            name='Attach Appendix III (Metadata format for Ongoing project)* Download Template for Appendix III',
            field=models.FileField(blank=True, null=True, upload_to='media/'),
        ),
        migrations.AlterField(
            model_name='files',
            name='Attach Cover Letter',
            field=models.FileField(blank=True, null=True, upload_to='media/'),
        ),
        migrations.AlterField(
            model_name='files',
            name='Attach the detailed Project proposal(Download Appendix I Template (.docx file)',
            field=models.FileField(blank=True, null=True, upload_to='media/'),
        ),
        migrations.AlterField(
            model_name='files',
            name='Attach the detailed Project proposal(Download Template (.docx file) ',
            field=models.FileField(blank=True, null=True, upload_to='media/'),
        ),
    ]
