# Generated by Django 3.2.5 on 2021-10-12 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0010_vehicleinfo_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicleinfo',
            name='smoke_pvc',
            field=models.CharField(blank=True, db_column='smoke_pvc', max_length=100),
        ),
        migrations.AddField(
            model_name='vehicleinfo',
            name='tailpipe',
            field=models.CharField(blank=True, db_column='tailpipe', max_length=100),
        ),
    ]
