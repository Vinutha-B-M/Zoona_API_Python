# Generated by Django 3.2.5 on 2021-10-04 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0013_default_payment_gatway'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serviceslist',
            name='input_mode',
        ),
        migrations.AddField(
            model_name='serviceslist',
            name='description',
            field=models.CharField(blank=True, db_column='Description', max_length=500),
        ),
    ]