from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.signup.as_view(), name="signup"),
    path('login/', views.login.as_view(), name="login"),
    path('forgot/', views.forgot.as_view(), name="forgot"),
    path('update/', views.update.as_view(), name="update"),
    path('user_info/', views.user_info.as_view(), name="update"),
]
