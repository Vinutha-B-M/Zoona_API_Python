from django.db import models
from service.models import ServicesList,Taxes,Fees,Discounts,TestType,MustHave
from customer.models import VehicleInfo
from users.models import UserType, UserInfo


# Create your models here.


class PaymentEntry(models.Model):
    Pending = 'Pending'
    Completed = 'Completed'
    Cancelled = 'cancelled'
    STATUS = (
        (Pending, 'Pending'),
        (Completed, 'Completed'),
        (Cancelled, 'cancelled')
    )
    Cash = 'Cash'
    Card = 'Card'
    Other = 'Other'
    MODE = (
        (Cash, 'Cash'),
        (Card, 'Card'),
        (Other, 'Other')
    )
    final_amount = models.FloatField(db_column='final_amount', max_length=200, blank=True, null=True)
    additional_comments = models.CharField(db_column='additional_comments', max_length=200, blank=True)
    tax_offered = models.FloatField(db_column='tax_offered', max_length=200, blank=True, null=True)
    amount_tendered = models.FloatField(db_column='amount_tendered', max_length=200, blank=True, null=True)
    changed_given = models.FloatField(db_column='changed_given', max_length=200, blank=True, null=True)
    discount_offered = models.FloatField(db_column='discount_offered', max_length=200, blank=True, null=True)
    payment_mode = models.CharField(db_column='payment_mode', max_length=10, choices=MODE, blank=True)
    status = models.CharField(db_column='status', max_length=10, choices=STATUS, blank=True)
    Vehicle = models.ForeignKey(VehicleInfo, db_column='Vehicle', null=True, on_delete=models.PROTECT)
    created_date = models.DateField(db_column='created_date', blank=True, null=True, auto_now_add=True)
    modified_date = models.DateField(db_column='modified_date', blank=True, null=True, auto_now_add=True)


class InvoiceItem(models.Model):
    service_item = models.ForeignKey(ServicesList, db_column='service_item', null=True, on_delete=models.PROTECT)
    service_name = models.CharField(db_column='service_name', blank=True, max_length=100)
    amount = models.FloatField(db_column='amount', blank=True, max_length=100, null=True)
    Payment = models.ForeignKey(PaymentEntry, db_column='payment', null=True, on_delete=models.PROTECT)

class TaxItem(models.Model):
    tax_item = models.ForeignKey(Taxes, db_column='tax_item', null=True, on_delete=models.PROTECT)
    tax_name = models.CharField(db_column='tax_name', blank=True, max_length=100)
    amount = models.CharField(db_column='amount', blank=True, max_length=100, null=True)
    Payment = models.ForeignKey(PaymentEntry, db_column='payment', null=True, on_delete=models.PROTECT)

class FeesItem(models.Model):
    fees_item = models.ForeignKey(Fees, db_column='fees_item', null=True, on_delete=models.PROTECT)
    fees_name = models.CharField(db_column='fees_name', blank=True, max_length=100)
    amount = models.CharField(db_column='amount', blank=True, max_length=100, null=True)
    Payment = models.ForeignKey(PaymentEntry, db_column='payment', null=True, on_delete=models.PROTECT)

class DiscountItem(models.Model):
    discount_item = models.ForeignKey(Discounts, db_column='discount_item', null=True, on_delete=models.PROTECT)
    offer_name = models.CharField(db_column='discount_name', blank=True, max_length=100)
    amount = models.CharField(db_column='amount', blank=True, max_length=100, null=True)
    Payment = models.ForeignKey(PaymentEntry, db_column='payment', null=True, on_delete=models.PROTECT)

class TestTypeItem(models.Model):
    test_item = models.ForeignKey(TestType, db_column='test_item', null=True, on_delete=models.PROTECT)
    test_type_name = models.CharField(db_column="test_type_name", max_length=100,blank=True)
    Payment = models.ForeignKey(PaymentEntry, db_column='payment', null=True, on_delete=models.PROTECT)

class MustHaveItem(models.Model):
    must_have_item = models.ForeignKey(MustHave, db_column='must_have_item', null=True, on_delete=models.PROTECT)
    must_have_name = models.CharField(db_column="must_have_name", max_length=100,blank=True)
    Payment = models.ForeignKey(PaymentEntry, db_column='payment', null=True, on_delete=models.PROTECT)
#
# class SquareTerminal(models.Model):
#     square_token = models.CharField(db_column="token", max_length=200, blank=True)
#     expires_at = models.CharField(db_column="expires_at", max_length=200, blank=True)
#     merchant_id = models.CharField(db_column="merchant_id", max_length=200, blank=True)
#     refresh_token = models.CharField(db_column="refresh_token", max_length=200, blank=True)
#     client = models.ForeignKey(UserInfo, db_column='client', null=True, on_delete=models.PROTECT)
#
#
# class SquareDevice(models.Model):
#     device_id = models.CharField(db_column="device", max_length=100, blank=True)
#     name = models.CharField(db_column="name_device", max_length=100, blank=True)
#     code = models.CharField(db_column="code", max_length=100, blank=True)
#     location = models.CharField(db_column="location", max_length=100, blank=True)
#     status = models.CharField(db_column="status", max_length=100, blank=True)
#     client = models.ForeignKey(UserInfo, db_column='client', null=True, on_delete=models.PROTECT)

# class SquareCredentials(models.Model):
#     client_id = models.CharField(db_column="client_id", max_length=100, blank=True)
#     client_secret = models.CharField(db_column="client_secret", max_length=100, blank=True)