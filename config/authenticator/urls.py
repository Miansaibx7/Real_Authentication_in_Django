from django.urls import path
from .views import (RegisterView, VerifyOTPView,LoginView,ForgotPasswordView,ResetPasswordView,)
from rest_framework_simplejwt.views import (TokenRefreshView)

urlpatterns = [
    # url for register
    path("register/", RegisterView.as_view(), name="register"),
    # url for VerifyOTP
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
    # url for Login
    path("login/", LoginView.as_view(), name="login"),
    # url for ForgotPassword
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    # url for ResetPassword
    path("reset-password/", ResetPasswordView.as_view(), name="reset-password"),

# refresh token endpoint for JWT authentication
    path('token/refresh/', TokenRefreshView.as_view()),
]