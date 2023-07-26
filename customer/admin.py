from django.contrib import admin
from .models import CustomerInfo, VehicleInfo, TestDetails

# Register your models here.
admin.site.register(CustomerInfo),
admin.site.register(VehicleInfo),
admin.site.register(TestDetails)
