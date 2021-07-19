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
]
