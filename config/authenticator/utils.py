import secrets
from django.core.mail import send_mail
from django.conf import settings

# Utility function to generate a 6-digit OTP
def generate_otp():
    return str(secrets.randbelow(900000) + 100000)

# Utility function to send OTP email
def send_email_otp(email, code):
    try:
        send_mail(subject="Your Verification Code", message=f"Your OTP code is: {code}",
            from_email=settings.EMAIL_HOST_USER, recipient_list=[email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"SMTP Setup Error: {e}") 
        # This prevents the registration endpoint from crashing 500 if email fails