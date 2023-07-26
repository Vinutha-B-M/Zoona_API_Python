# Generated by Django 3.2.5 on 2021-07-28 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0004_alter_serviceslist_amount'),
        ('payment', '0004_auto_20210726_1517'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaxItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tax_name', models.CharField(blank=True, db_column='service_name', max_length=100)),
                ('amount', models.CharField(blank=True, db_column='amount', max_length=100, null=True)),
                ('Payment', models.ForeignKey(db_column='payment', null=True, on_delete=django.db.models.deletion.PROTECT, to='payment.paymententry')),
                ('tax_item', models.ForeignKey(db_column='service_item', null=True, on_delete=django.db.models.deletion.PROTECT, to='service.serviceslist')),
            ],
        ),
        migrations.CreateModel(
            name='FeesItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fees_name', models.CharField(blank=True, db_column='service_name', max_length=100)),
                ('amount', models.CharField(blank=True, db_column='amount', max_length=100, null=True)),
                ('Payment', models.ForeignKey(db_column='payment', null=True, on_delete=django.db.models.deletion.PROTECT, to='payment.paymententry')),
                ('fees_item', models.ForeignKey(db_column='service_item', null=True, on_delete=django.db.models.deletion.PROTECT, to='service.serviceslist')),
            ],
        ),
        migrations.CreateModel(
            name='DiscountItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount_name', models.CharField(blank=True, db_column='service_name', max_length=100)),
                ('amount', models.CharField(blank=True, db_column='amount', max_length=100, null=True)),
                ('Payment', models.ForeignKey(db_column='payment', null=True, on_delete=django.db.models.deletion.PROTECT, to='payment.paymententry')),
                ('discount_item', models.ForeignKey(db_column='service_item', null=True, on_delete=django.db.models.deletion.PROTECT, to='service.serviceslist')),
            ],
        ),
    ]
