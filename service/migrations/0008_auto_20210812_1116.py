# Generated by Django 3.2.5 on 2021-08-12 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0007_squarecredential'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receiptcontent',
            name='company_name',
        ),
        migrations.RemoveField(
            model_name='receiptcontent',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='receiptcontent',
            name='website_url',
        ),
        migrations.AddField(
            model_name='receiptcontent',
            name='company_logo',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='receiptcontent',
            name='email',
            field=models.CharField(blank=True, db_column='email', max_length=200),
        ),
    ]
