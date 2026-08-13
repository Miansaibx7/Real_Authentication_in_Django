from django.urls import path
from .views import RegisterView, VerifyOTPView,LoginView,ForgotPasswordView,ResetPasswordView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Endpoint for register
    path("register/", RegisterView.as_view(), name="register"),
    # Endpoint  for VerifyOTP
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
    # Endpoint for Login
    path("login/", LoginView.as_view(), name="login"),
    # Endpoint for ForgotPassword
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    # Endpoint for ResetPassword
    path("reset-password/", ResetPasswordView.as_view(), name="reset-password"),
    # Refresh token endpoint for JWT authentication
    path('token/refresh/', TokenRefreshView.as_view()),
]