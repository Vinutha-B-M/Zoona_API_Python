from django.conf.urls import url
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('invoice_entry/', views.payment_entry.as_view(), name="invoice_entry"),
    path('update_invoice_entry/', views.update_payment_entry.as_view(), name="update_invoice_entry"),
    path('payment_validate/', views.payment_validate.as_view(), name="payment_validate"),
    path('order_list/', views.order_list.as_view(), name="order_list"),
    path('order_list_page/', views.order_list_page.as_view(), name="order_list_page"),
    path('confirm_list/', views.confirm_list.as_view(), name="confirm_list"),
    path('datewise_order_list/', views.datewise_order_list.as_view(), name="datewise_order_list"),
    path('custom_order_list/', views.custom_order_list.as_view(), name="datewise_order_list"),
    path('datewise_customer_list/', views.datewise_customer_list.as_view(), name="datewise_customer_list"),
    path('delete_vehicle/', views.delete_vehicle.as_view(), name="delete_vehicle"),
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
    path('recreate_device/', views.recreate_device.as_view(), name="recreate_device"),
    path('create_terminal_checkout/',views.create_terminal_checkout.as_view(), name="create_terminal_checkout"),
    path('delete_device/', views.delete_device.as_view(), name="delete_device"),
    path('fortispay_credentials/', views.fortispay_credentials.as_view(), name="fortispay_credentials"),
    path('fortispay_update_credentials/', views.fortispay_update_credentials.as_view(), name="fortispay_update_credentials"),
    path('fortispay_terminal_list/', views.fortispay_terminal_list.as_view(), name="fortispay_terminal_list"),
    path('fortispay/', views.fortispay.as_view(), name="fortispay"),
    path('get_router_transaction/', views.get_router_transaction.as_view(), name="get_router_transaction"),
    path('stats_daily/',views.stats_daily.as_view(), name="stats_daily"),
    path('stats_monthly/',views.stats_monthly.as_view(), name="stats_monthly"),
    path('stats_weekly/',views.stats_weekly.as_view(), name="stats_weekly"),
    path('stats_services/',views.stats_services.as_view(), name="stats_services"),
    path('stats_overall/',views.stats_overall.as_view(), name="stats_overall"),
    path('stats_filter/',views.stats_filter.as_view(), name="stats_filter"),
    path('filter_services/',views.filter_services.as_view(), name="filter_services"),
    path('mail_to_customer/',views.mail_to_customer.as_view(), name="mail_to_customer"),
    path('delete_order/',views.delete_order.as_view(), name="delete_order"),
    path('daily/', views.daily.as_view(), name="daily"),
    path('monthly/', views.monthly.as_view(), name="monthly"),
    path('weekly/', views.weekly.as_view(), name="weekly"),
    path('test/', views.test.as_view(), name="test"),
    path('order_daily/',views.order_daily.as_view(),name="order_daily"),
    path('order_weekly/',views.order_weekly.as_view(),name="order_weekly"),
    path('order_monthly/',views.order_monthly.as_view(),name="order_monthly"),
]