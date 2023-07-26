from django.conf.urls import url
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('', views.home, name='home'),
    path('customer/', views.Customer.as_view(), name="customer"),
    path('add_customer_list/', views.add_Customer_List.as_view(), name="add_customer_list"),
    path('update_customer_list/', views.update_customer_list.as_view(), name="update_customer_list"),
    path('signature/',views.signature),
    path('vehicle_signature/',views.vehicle_signature),
    path('fetch_customer_info/', views.fetch_customer_info.as_view(), name="fetch_customer_info"),
    path('vehicle_list/', views.Vehicle_List.as_view(), name="vehicle_list"),
    path('customer_list/', views.customer_list.as_view(), name="customer_list"),
    path('add_vehicle_list/', views.add_Vehicle_List.as_view(), name="add_vehicle_list"),
    path('update_vehicle_list/', views.update_vehicle_list.as_view(), name="update_vehicle_list"),
    path('test_list/', views.Test_List.as_view(), name="test_list"),
    path('vehicle_info/', views.vehicle_info.as_view(), name="vehicle_info"),
    path('customers_filter/', views.customers_filter.as_view(), name="customers_filter"),
    path('vehicle_filter/', views.vehicle_filter.as_view(), name="vehicle_filter"),
    path('terms_update/', views.update_terms.as_view(), name="terms_update"),
    path('update_customer_status/', views.status_changed_customer.as_view(), name="update_customer_status"),
    path('update_vehicle_status/', views.status_changed_vehicle.as_view(), name="update_vehicle_status"),
]
