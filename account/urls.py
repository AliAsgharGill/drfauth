from django.urls import path
from .views import UserProfileView, UserRegistrationView, UserLoginView, UserChangePasswordView, SendResetPasswordEmailView, ForgotPasswordView
urlpatterns = [
    path('register/', UserRegistrationView.as_view() , name='register'),
    path('login/', UserLoginView.as_view() , name='login'),
    path('profile/', UserProfileView.as_view() , name='profile'),
    path('change-password/', UserChangePasswordView.as_view() , name='change-password'),
    path('send-reset-password-email/', SendResetPasswordEmailView.as_view() , name='send-reset-password-email'),
    path('forgot-password/<uid>/<token>/', ForgotPasswordView.as_view() , name='forgot-password')
]
