from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from . import views

app_name = 'users'

urlpatterns = [
    path('', views.main, name='main'),
    path('register', views.register, name='register'),
    path('login', views.user_login, name='login'),
    path('edit', views.edit_profile, name='edit'),
    path('logout', views.user_logout, name='logout'),
    path('activate-user/<uidb64>/<token>', views.activate_user, name='activate'),
    # Password change section
    path(
        'password_change/',
        auth_views.PasswordChangeView.as_view(template_name='account/password_change/password_change_form.html'),
        name='password_change',
    ),
    path(
        'password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(template_name='account/password_change/password_change_done.html'),
        name='password_change_done',
    ),
    # Password reset section
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='account/password_change/password_reset_form.html',
            email_template_name='account/password_change/password_reset_email.html',
            success_url=reverse_lazy('users:password_reset_done'),
        ),
        name='password_reset',
    ),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='account/password_change/password_reset_done.html'),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='account/password_change/password_reset_confirm.html',
            success_url=reverse_lazy('users:password_reset_complete'),
        ),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
        name='password_reset_complete',
    ),
    # Social auth
    path(
        'add-entrada/<id>',
        views.add_favorite,
        name='add-favoritos',
    ),
]
