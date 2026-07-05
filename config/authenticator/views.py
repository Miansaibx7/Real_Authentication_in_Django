
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, get_user_model

from .models import EmailOTP, PasswordResetOTP
from .serializers import RegisterSerializer, LoginSerializer
from .utils import generate_otp, send_email_otp

from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import F
from django.contrib.auth.password_validation import validate_password

from rest_framework.permissions import AllowAny
from rest_framework import status

User = get_user_model()

# ---------------- REGISTER --------------------------------
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            code = generate_otp()
            EmailOTP.objects.update_or_create(user=user, defaults={"code": code, "attempts": 0})
            send_email_otp(user.email, code)

            return Response({"message": "OTP sent to the email"},status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------- VERIFY EMAIL OTP ---------------------------
class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")

        #  input validation
        if not email or not code:
            return Response({"error": "Email and OTP required"},status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            otp = EmailOTP.objects.get(user=user)
        except (User.DoesNotExist, EmailOTP.DoesNotExist):
            return Response({"error": "Invalid email or OTP"},status=status.HTTP_400_BAD_REQUEST)

        #  attempt limit
        if otp.attempts >= 5:
            return Response({"error": "Too many attempts"},status=status.HTTP_429_TOO_MANY_REQUESTS)

        #  expiry check
        if otp.is_expired():
            otp.delete()
            return Response({"error": "OTP expired"},status=status.HTTP_400_BAD_REQUEST)

        #  safer comparison
        if str(otp.code).strip() != str(code).strip():
            EmailOTP.objects.filter(id=otp.id).update(
                attempts=F('attempts') + 1
            )
            otp.refresh_from_db()

            return Response({"error": "Invalid OTP"},status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.is_verified = True
        user.save()
        otp.delete()

        return Response({"message": "Account verified successfully..."},status=status.HTTP_200_OK)


# ---------------- LOGIN (JWT) ------------------------------------
class LoginView(APIView):

    permission_classes = [AllowAny]
    def post(self, request):

        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            user = authenticate(username=email,password=password)
            if not user:
                return Response({"error": "Invalid credentials"},status=status.HTTP_401_UNAUTHORIZED)

            if not user.is_verified:
                return Response({"error": "Email not verified"},status=status.HTTP_403_FORBIDDEN)

            refresh = RefreshToken.for_user(user)
            return Response({"refresh": str(refresh),"access": str(refresh.access_token),})

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# ---------------- FORGOT PASSWORD (Send OTP) ------------------------------------
class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"message":"If the email exists, OTP has been sent"},status=status.HTTP_200_OK)

        code = generate_otp()
        PasswordResetOTP.objects.update_or_create(user=user,defaults={"code": code, "attempts": 0})
        send_email_otp(email, code)
        return Response({"message": "OTP sent successfully"},status=status.HTTP_200_OK)


# ---------------- RESET PASSWORD ------------------------------------
class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        email = request.data.get("email")
        code = request.data.get("code")
        new_password = request.data.get("new_password")
        try:
            user = User.objects.get(email=email)
            otp = PasswordResetOTP.objects.get(user=user)
        except (User.DoesNotExist, PasswordResetOTP.DoesNotExist):
            return Response({"error": "Invalid request"},status=status.HTTP_400_BAD_REQUEST)

        if otp.is_expired():
            otp.delete()
            return Response({"error": "OTP expired"},status=status.HTTP_400_BAD_REQUEST)

        if otp.code != code:
            otp.attempts += 1
            otp.save()
            return Response({"error": "Invalid OTP"},status=status.HTTP_400_BAD_REQUEST)

        validate_password(new_password)
        user.set_password(new_password)
        user.save()
        otp.delete()
        return Response({"message": "Password reset successful"},status=status.HTTP_200_OK)
    

# ---------------- LOGOUT (Blacklist JWT) ------------------------------------
class LogoutView(APIView):

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"error": "Refresh token required"},status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid token"},status=status.HTTP_400_BAD_REQUEST)
