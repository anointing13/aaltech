from django.urls import path
from .views import signup, user_login, user_logout
from django.contrib.auth import views as auth_views
from .views import CustomPasswordResetView, CustomPasswordResetConfirmView  # Ensure the custom view is imported

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('password_reset/', CustomPasswordResetView.as_view(
        template_name='accounts/password_reset.html',
        email_template_name='registration/password_reset_email.html',
        extra_email_context={'site_name': 'ANTE OMNIA LIMITED'}
    ), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(  # Use the custom view here
        template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
]



