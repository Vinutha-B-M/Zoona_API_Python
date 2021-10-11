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
        (Other, 'Other'),
    )
    invoice_id = models.CharField(db_column="invoice", max_length=100, blank=True, null=True)
    final_amount = models.FloatField(db_column='final_amount', max_length=200, blank=True, null=True)
    card_amount = models.FloatField(db_column='card_amount', max_length=200, blank=True, null=True)
    additional_comments = models.CharField(db_column='additional_comments', max_length=200, blank=True)
    tax_offered = models.FloatField(db_column='tax_offered', max_length=200, blank=True, null=True)
    amount_tendered = models.FloatField(db_column='amount_tendered', max_length=200, blank=True, null=True)
    changed_given = models.FloatField(db_column='changed_given', max_length=200, blank=True, null=True)
    discount_offered = models.FloatField(db_column='discount_offered', max_length=200, blank=True, null=True)
    payment_mode = models.CharField(db_column='payment_mode', max_length=100, choices=MODE, blank=True)
    status = models.CharField(db_column='status', max_length=100, choices=STATUS, blank=True)
    Vehicle = models.ForeignKey(VehicleInfo, db_column='Vehicle', null=True, on_delete=models.PROTECT)
    fly_fees = models.FloatField(db_column='fly_fees',default=0)
    fly_discount = models.FloatField(db_column='fly_discount',default=0)
    test_results = models.CharField(db_column='Test_Results', max_length=30, blank=True)
    inception_performed = models.BooleanField(db_column='inception_performed', default=False)
    lf = models.CharField(db_column='LF', max_length=30,blank=True)
    rf = models.CharField(db_column='RF', max_length=30, blank=True)
    lr = models.CharField(db_column='LR', max_length=30, blank=True)
    rr = models.CharField(db_column='RR', max_length=30, blank=True)
    inception_declined = models.BooleanField(db_column='inception_declined',default=False)
    reasons = models.CharField(db_column='Reasons', max_length=30,blank=True)
    initials = models.CharField(db_column='Initials', max_length=30, blank=True)
    created_date = models.DateTimeField(db_column='created_date', blank=True, null=True, auto_now_add=True)
    modified_date = models.DateTimeField(db_column='modified_date', blank=True, null=True, auto_now_add=True)


class InvoiceItem(models.Model):
    service_item = models.ForeignKey(ServicesList, db_column='service_item', null=True, on_delete=models.PROTECT)
    service_name = models.CharField(db_column='service_name', blank=True, max_length=100)
    amount = models.FloatField(db_column='amount', blank=True, max_length=100, null=True)
    Payment = models.ForeignKey(PaymentEntry, db_column='payment', null=True, on_delete=models.PROTECT)
    created_date = models.DateTimeField(db_column='created_date', blank=True, null=True, auto_now_add=True)

class TaxItem(models.Model):
    tax_item = models.ForeignKey(Taxes, db_column='tax_item', null=True, on_delete=models.PROTECT)
    tax_name = models.CharField(db_column='tax_name', blank=True, max_length=100)
    amount = models.CharField(db_column='amount', blank=True, max_length=100, null=True)
    Payment = models.ForeignKey(PaymentEntry, db_column='payment', null=True, on_delete=models.PROTECT)
    created_date = models.DateTimeField(db_column='created_date', blank=True, null=True, auto_now_add=True)

class FeesItem(models.Model):
    fees_item = models.ForeignKey(Fees, db_column='fees_item', null=True, on_delete=models.PROTECT)
    fees_name = models.CharField(db_column='fees_name', blank=True, max_length=100)
    amount = models.CharField(db_column='amount', blank=True, max_length=100, null=True)
    Payment = models.ForeignKey(PaymentEntry, db_column='payment', null=True, on_delete=models.PROTECT)
    created_date = models.DateTimeField(db_column='created_date', blank=True, null=True, auto_now_add=True)

class DiscountItem(models.Model):
    discount_item = models.ForeignKey(Discounts, db_column='discount_item', null=True, on_delete=models.PROTECT)
    offer_name = models.CharField(db_column='discount_name', blank=True, max_length=100)
    amount = models.CharField(db_column='amount', blank=True, max_length=100, null=True)
    Payment = models.ForeignKey(PaymentEntry, db_column='payment', null=True, on_delete=models.PROTECT)
    created_date = models.DateTimeField(db_column='created_date', blank=True, null=True, auto_now_add=True)

class TestTypeItem(models.Model):
    test_item = models.ForeignKey(TestType, db_column='test_item', null=True, on_delete=models.PROTECT)
    test_type_name = models.CharField(db_column="test_type_name", max_length=100,blank=True)
    Payment = models.ForeignKey(PaymentEntry, db_column='payment', null=True, on_delete=models.PROTECT)

class MustHaveItem(models.Model):
    must_have_item = models.ForeignKey(MustHave, db_column='must_have_item', null=True, on_delete=models.PROTECT)
    must_have_name = models.CharField(db_column="must_have_name", max_length=100,blank=True)
    Payment = models.ForeignKey(PaymentEntry, db_column='payment', null=True, on_delete=models.PROTECT)


class SquareTerminalCheckout(models.Model):
    checkout_id = models.CharField(db_column="checkout_id", max_length=200, blank=True)
    client = models.ForeignKey(UserInfo, db_column='client', null=True, on_delete=models.PROTECT)
    payment = models.ForeignKey(PaymentEntry, db_column='Payment', null=True, on_delete=models.PROTECT)


class SquareDevice(models.Model):
    square_id = models.CharField(db_column="square_id", max_length=100, blank=True)
    device_id = models.CharField(db_column="device_id", max_length=100, blank=True,null=True)
    name = models.CharField(db_column="name_device", max_length=100, blank=True)
    code = models.CharField(db_column="code", max_length=100, blank=True)
    location = models.CharField(db_column="location", max_length=100, blank=True)
    status = models.CharField(db_column="status", max_length=100, blank=True)
    client = models.ForeignKey(UserInfo, db_column='client', null=True, on_delete=models.PROTECT)

class FortisPayCredentials(models.Model):
    username=models.CharField(db_column="username",max_length=100,blank=True)
    password=models.CharField(db_column="password",max_length=100,blank=True)
    domain=models.CharField(db_column="domain", max_length=100,blank=True)
    client = models.ForeignKey(UserInfo, db_column='client', null=True, on_delete=models.PROTECT)