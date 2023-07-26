from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.signup.as_view(), name="signup"),
    path('login/', views.login.as_view(), name="login"),
    path('forgot/', views.forgot.as_view(), name="forgot"),
    path('update/', views.update.as_view(), name="update"),
    path('user_info/', views.user_info.as_view(), name="user_info"),
    path('update_user_info/', views.update_user_info.as_view(), name="update_user_info"),
    path('add_user/', views.add_user.as_view(), name="add_user"),
    path('users/', views.users_data.as_view(), name="users"),
    path('update_users/', views.update_users.as_view(), name="update_users"),
    path('delete_users/', views.delete_users.as_view(), name="delete_users"),
    path('company_logo/',views.company_logo),
    path('confirm_password/', views.confirm_password.as_view(), name="confirm_password"),
]
