# Generated by Django 3.2.5 on 2021-08-17 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_vehicleinfo_engine_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicleinfo',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, db_column='created_date', null=True),
        ),
    ]