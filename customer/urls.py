from django.conf.urls import url
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('', views.home, name='home'),
    path('customer_list/', views.Customer_List.as_view(), name="customer_list"),
    path('vehicle_list/', views.Vehicle_List.as_view(), name="vehicle_list"),
    path('test_list/', views.Test_List.as_view(), name="test_list")
]
