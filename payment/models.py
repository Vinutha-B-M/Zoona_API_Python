from django.db import models

# Create your models here.

# class PaymentEntry(models.Model):
#     Auto = 'Auto'
#     Standard = 'Standard'
#     STATUS = (
#         (Auto, 'Auto'),
#         (Standard, 'Standard')
#     )
#     vin = models.CharField(db_column='vin', max_length=200, blank=True)
#     engine = models.CharField(db_column='engine', max_length=200, blank=True)
#     cylinder = models.CharField(db_column='cylinder', max_length=200, blank=True)
#     Transmission = models.CharField(db_column='Transmission', max_length=10, choices=STATUS, blank=True)
#     customer_id = models.ForeignKey(CustomerInfo, db_column='customer_id', null=True, on_delete=models.PROTECT)
#     created_date = models.DateField(db_column='created_date', blank=True, null=True, auto_now_add=True)