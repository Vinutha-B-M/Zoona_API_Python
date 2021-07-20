from django.conf.urls import url
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('receipt_content/', views.receipt_content.as_view(), name="receipt_content"),
    path('taxes/', views.taxes.as_view(), name="taxes"),
    path('discounts/', views.discounts.as_view(), name="discounts"),
    path('services/', views.services.as_view(), name="services"),
    path('defaults/', views.defaults.as_view(), name="defaults"),
    path('add_receipt_content/', views.add_receipt_content.as_view(), name="add_receipt_content"),
    path('add_taxes/', views.add_taxes.as_view(), name="add_taxes"),
    path('add_discounts/', views.add_discounts.as_view(), name="add_discounts"),
    path('add_services/', views.add_services.as_view(), name="add_services"),
    path('add_defaults/', views.add_defaults.as_view(), name="add_defaults"),
    path('delete_taxes/', views.delete_taxes.as_view(), name="delete_taxes"),
    path('delete_discounts/', views.delete_discounts.as_view(), name="delete_discounts"),
    path('delete_services/', views.delete_services.as_view(), name="delete_services"),
    path('update_taxes/', views.update_taxes.as_view(), name="update_taxes"),
    path('update_discounts/', views.update_discounts.as_view(), name="update_discounts"),
    path('update_services/', views.update_services.as_view(), name="update_services"),
]
