from django.conf.urls import url
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('device_list/', views.device_list.as_view(), name="device_list"),
    # path('get_device_code/', views.get_device_code.as_view(), name="get_device_code"),
    path('invoice_entry/', views.payment_entry.as_view(), name="invoice_entry"),
    path('payment_validate/', views.payment_validate.as_view(), name="payment_validate"),

]