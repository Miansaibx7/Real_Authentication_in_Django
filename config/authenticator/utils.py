# (EMAIL + OTP LOGIC)
from django.core.mail import send_mail
import random

def generate_otp():
    """Generates a 6-digit OTP."""
    return str(random.randint(100000, 999999))


# Sends the OTP to the user's email.
def send_email_otp(email, code):
    send_mail(
        "Your Verification Code",
        f"Your OTP is {code}",
        "yourgmail@gmail.com",
        [email],
        fail_silently=False,
    )