from django.conf.urls import url
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('invoice_entry/', views.payment_entry.as_view(), name="invoice_entry"),
    path('update_invoice_entry/', views.update_payment_entry.as_view(), name="update_invoice_entry"),
    path('payment_validate/', views.payment_validate.as_view(), name="payment_validate"),
    path('order_list/', views.order_list.as_view(), name="order_list"),
    path('confirm_list/', views.confirm_list.as_view(), name="confirm_list"),
    path('datewise_order_list/', views.datewise_order_list.as_view(), name="datewise_order_list"),
    path('datewise_customer_list/', views.datewise_customer_list.as_view(), name="datewise_customer_list"),
    path('delete_customer/', views.delete_customer.as_view(), name="delete_customer"),
    path('sales/', views.total_sales.as_view(), name="sales"),
    path('order_invoice/', views.order_invoice.as_view(), name="order_invoice"),
    path('generic_tables/', views.generic_tables.as_view(), name="generic_tables"),
    # path('device_list/', views.device_list.as_view(), name="device_list"),
    # path('get_device_code/', views.get_device_code.as_view(), name="get_device_code"),
    # path('create_token/', views.create_token.as_view(), name="create_token"),
    # path('renew_token/', views.renew_token.as_view(), name="renew_token"),
    # path('list_device/', views.list_device.as_view(), name="list_device"),
    path('get_device/', views.get_device.as_view(), name="get_device"),
    path('create_device/', views.create_device.as_view(), name="create_device"),
    path('create_terminal_checkout/',views.create_terminal_checkout.as_view(), name="create_terminal_checkout")
]