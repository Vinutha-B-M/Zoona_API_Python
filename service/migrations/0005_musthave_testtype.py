# Generated by Django 3.2.5 on 2021-07-29 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0004_alter_serviceslist_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='MustHave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('must_have_name', models.CharField(blank=True, db_column='must_have_name', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TestType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_type_name', models.CharField(blank=True, db_column='test_type_name', max_length=100)),
            ],
        ),
    ]
