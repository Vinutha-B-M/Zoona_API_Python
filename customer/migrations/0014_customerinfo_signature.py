# Generated by Django 3.2.5 on 2021-11-18 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0013_vehicleinfo_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerinfo',
            name='signature',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
