# (CORE LOGIC)
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from .models import EmailOTP, PasswordResetOTP
from .serializers import RegisterSerializer, LoginSerializer
from .utils import generate_otp, send_email_otp

from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.permissions import AllowAny

User = get_user_model()

# ---------------- REGISTER --------------------------------
class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            code = generate_otp()
            EmailOTP.objects.create(user=user, code=code)
            send_email_otp(user.email, code)

            return Response({"message": "OTP sent to email"})
        return Response(serializer.errors, status=400)


# ---------------- VERIFY EMAIL OTP ---------------------------
class VerifyOTPView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")

        user = User.objects.get(email=email)
        otp = EmailOTP.objects.get(user=user)

        if otp.code == code and not otp.is_expired():
            user.is_active = True
            user.is_verified = True
            user.save()
            otp.delete()
            return Response({"message": "Account verified"})
        return Response({"error": "Invalid OTP"})


# ---------------- LOGIN (JWT) ------------------------------------
class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(username=email, password=password)

            if user:
                if not user.is_verified:
                    return Response({"error":"Email not verified"})
                
                refresh = RefreshToken.for_user(user)
                
                # Remember me logic
                remember = request.data.get('remember', False)

                if remember:
                    refresh.set_exp(lifetime=60*60*24*30)  # 30 days
                else:
                    refresh.set_exp(lifetime=60*60*1) # 1 hour

                return Response({"refresh": str(refresh),
                                 "access": str(refresh.access_token),})
            return Response({"error": "Invalid credentials"})
        return Response(serializer.errors, status=400)
    

# ---------------- FORGOT PASSWORD (SEND OTP) -----------------------------
class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get("email")
        user = User.objects.get(email=email)
        
        code = generate_otp() 
        PasswordResetOTP.objects.create(user=user, code=code)
        send_email_otp(email, code)

        return Response({"message": "OTP sent to email"})
    

# ---------------- RESET PASSWORD --------------------------------------------
class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        new_password = request.data.get('new_password')

        user = User.objects.get(email=email)
        otp = PasswordResetOTP.objects.get(user=user)
        if otp.code == code and not otp.is_expired():
            user.set_password(new_password)
            user.save()
            otp.delete()
            return Response({"message": "Password reset successfully"})

        return Response({"error": "Invalid OTP"})

