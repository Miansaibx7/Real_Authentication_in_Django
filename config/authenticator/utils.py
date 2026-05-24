import secrets

from django.core.mail import send_mail

from django.conf import settings


def generate_otp():

    return str(
        secrets.randbelow(900000) + 100000
    )


def send_email_otp(email, code):

    send_mail(
        "Your Verification Code",
        f"Your OTP is {code}",
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )