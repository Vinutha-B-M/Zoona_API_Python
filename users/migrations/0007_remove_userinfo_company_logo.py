# Generated by Django 3.2.5 on 2021-08-12 05:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_userinfo_company_logo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='company_logo',
        ),
    ]
