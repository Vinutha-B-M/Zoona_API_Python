from django.db import models


# Create your models here.
class UserInfo(models.Model):
    company_name = models.CharField(db_column='company_name', max_length=200, blank=True)
    created_date = models.DateField(db_column='created_date', blank=True, null=True, auto_now_add=True)


class UserType(models.Model):
    full_name = models.CharField(db_column='full_name', max_length=200, blank=True)
    phone_number = models.CharField(db_column='phone_number', max_length=200, blank=True)
    username = models.CharField(db_column='username', max_length=200, blank=True)
    password = models.CharField(db_column='password', max_length=100, blank=True)
    is_admin = models.BooleanField(db_column='is_admin', default=False)
    created_date = models.DateField(db_column='created_date', blank=True, null=True, auto_now_add=True)
    profile = models.ImageField(blank=True,null=True)
    userinfo = models.ForeignKey(UserInfo, db_column='userinfo', null=True, on_delete=models.PROTECT)




