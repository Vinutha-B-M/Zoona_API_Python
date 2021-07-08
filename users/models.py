from django.db import models


# Create your models here.
class UserInfo(models.Model):
    full_name = models.CharField(db_column='full_name', max_length=200, blank=True)
    username = models.CharField(db_column='username', max_length=200, blank=True)
    password = models.CharField(db_column='password', max_length=100, blank=True)
    created_date = models.DateField(db_column='created_date', blank=True, null=True, auto_now_add=True)