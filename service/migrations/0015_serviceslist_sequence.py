# Generated by Django 3.2.5 on 2021-10-06 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0014_auto_20211004_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceslist',
            name='sequence',
            field=models.IntegerField(blank=True, db_column='sequence', null=True),
        ),
    ]
