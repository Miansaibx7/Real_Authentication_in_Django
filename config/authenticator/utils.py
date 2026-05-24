import secrets

from django.core.mail import send_mail
from django.conf import settings


def generate_otp():

    return str(secrets.randbelow(900000) + 100000)  # Generate a 6-digit OTP


def send_email_otp(email, code):

    send_mail(
        subject="Your Verification Code",
        message=f"Your OTP code is: {code}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )