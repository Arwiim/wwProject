from django.urls import path
from django.contrib.auth import views

from . import views

app_name = 'users'

urlpatterns = [
    path('', views.main, name='main'),
    path('register', views.register, name='register'),
    path('login', views.user_login, name='login'),
    path('edit', views.edit_profile, name='edit'),
    path('logout', views.user_logout, name='logout'),
    path('recover', views.user_recovery_password, name='recover_password'),
    path('activate-user/<uidb64>/<token>',views.activate_user, name='activate'),
    path('recover-confirm', views.user_password_confirm, name='recover_password_confirm'),
]
