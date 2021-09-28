# Generated by Django 3.2.5 on 2021-09-20 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0014_fortispaycredentials'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymententry',
            name='payment_mode',
            field=models.CharField(blank=True, choices=[('Cash', 'Cash'), ('Card', 'Card'), ('Other', 'Other')], db_column='payment_mode', max_length=100),
        ),
        migrations.AlterField(
            model_name='paymententry',
            name='status',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('cancelled', 'cancelled')], db_column='status', max_length=100),
        ),
    ]