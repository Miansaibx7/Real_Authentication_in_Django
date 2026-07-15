
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from datetime import timedelta


class UserManager(BaseUserManager):
# Create custom user manager for email authentication
    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError("Email address is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        extra_fields['is_verified'] = True
        extra_fields['is_active'] = True

        return self.create_user(email, password, **extra_fields)

# Custom User Model with email as username field and verification status
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email

# EmailOTP Send Model for registration 
class EmailOTP(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    attempts = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self)-> None:
        return timezone.now() > self.created_at + timedelta(minutes=10)

    def __str__(self):
        return f"{self.user.email} Email OTP"

# Reset Password OTP Model  
class PasswordResetOTP(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    attempts = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)

    def __str__(self):
        return f"{self.user.email} Reset OTP"
    