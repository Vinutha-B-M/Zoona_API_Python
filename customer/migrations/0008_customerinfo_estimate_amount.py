# Generated by Django 3.2.5 on 2021-10-06 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0007_termsitems'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerinfo',
            name='estimate_amount',
            field=models.FloatField(blank=True, db_column='estimate_amount', max_length=100, null=True),
        ),
    ]