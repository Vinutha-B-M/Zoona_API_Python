# Generated by Django 3.2.5 on 2022-08-30 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0019_paymententry_transaction_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymententry',
            name='signature',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]