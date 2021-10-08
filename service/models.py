from django.db import models
from users.models import UserInfo


# Create your models here.

class ReceiptContent(models.Model):
    company_logo = models.FileField(blank=True, null=True)
    image_name = models.CharField(db_column='image_name', max_length=300,blank=True)
    address = models.CharField(db_column='address', max_length=200, blank=True)
    email = models.CharField(db_column='email', max_length=200, blank=True)
    footer_note = models.CharField(db_column='footer_note', max_length=200, blank=True)
    client = models.ForeignKey(UserInfo, db_column='customer_id', null=True, on_delete=models.PROTECT)


class Taxes(models.Model):
    tax_value = models.CharField(db_column='tax_value', max_length=20, blank=True,null=True)
    tax_name = models.CharField(db_column='tax_name', max_length=200, blank=True)
    visible = models.BooleanField(db_column='visible', default=False)
    client = models.ForeignKey(UserInfo, db_column='customer_id', null=True, on_delete=models.PROTECT)

class Fees(models.Model):
    fees_value = models.CharField(db_column='fees_value', max_length=20, blank=True)
    fees_name = models.CharField(db_column='fees_name', max_length=200, blank=True)
    visible = models.BooleanField(db_column='visible', default=False)
    client = models.ForeignKey(UserInfo, db_column='customer_id', null=True, on_delete=models.PROTECT)

class Discounts(models.Model):
    discount_value = models.CharField(db_column='discount_value', max_length=20, blank=True)
    offer_name = models.CharField(db_column='offer_name', max_length=50, blank=True)
    client = models.ForeignKey(UserInfo, db_column='customer_id', null=True, on_delete=models.PROTECT)

class ServicesList(models.Model):
    service_name = models.CharField(db_column='service_name', max_length=200, blank=True)
    description = models.CharField(db_column='Description', max_length=500, blank=True)
    amount = models.FloatField(db_column='amount', max_length=30, blank=True,null=True)
    sequence = models.IntegerField(db_column='sequence',blank=True,null=True)
    client = models.ForeignKey(UserInfo, db_column='customer_id', null=True, on_delete=models.PROTECT)


class Default(models.Model):
    currency = models.CharField(db_column='currency', max_length=200, blank=True)
    langaugge = models.CharField(db_column='langaugge', max_length=200, blank=True)
    time_zone = models.CharField(db_column='time_zone', max_length=400, blank=True)
    display_time = models.CharField(db_column='display_time', max_length=200, blank=True)
    date_format = models.CharField(db_column='date_format', max_length=200, blank=True)
    print_format = models.CharField(db_column='Print_format', max_length=50, blank=True)
    payment_gatway = models.CharField(db_column='payment_gatway', max_length=100, blank=True)
    client = models.ForeignKey(UserInfo, db_column='customer_id', null=True, on_delete=models.PROTECT)

class TestType(models.Model):
    test_type_name=models.CharField(db_column="test_type_name", max_length=100, blank=True)

class MustHave(models.Model):
    must_have_name = models.CharField(db_column="must_have_name", max_length=100, blank=True)

class CashDiscount(models.Model):
    cash_discount_amount = models.CharField(db_column='cash_discount_amount', max_length=200, blank=True)
    visible = models.BooleanField(db_column='visible', default=False)
    client = models.ForeignKey(UserInfo, db_column='customer_id', null=True, on_delete=models.PROTECT)

class SquareCredential(models.Model):
    application_id = models.CharField(db_column='application_id', max_length=100, blank=True)
    application_secret = models.CharField(db_column='application_secret', max_length=100, blank=True)
    location_id = models.CharField(db_column='location_id', max_length=100, blank=True)
    accees_token = models.CharField(db_column='accees_token', max_length=100, blank=True)
    client = models.ForeignKey(UserInfo, db_column='customer_id', null=True, on_delete=models.PROTECT)

class TermCondition(models.Model):
    term_text = models.CharField(db_column='term_text', max_length=2000, blank=True)
    visible = models.BooleanField(db_column='visible', default=False)
    client = models.ForeignKey(UserInfo, db_column='customer_id', null=True, on_delete=models.PROTECT)