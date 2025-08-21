import random
from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    UserManager,
)
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timedelta
from django.utils import timezone
EXPIRATION_TIME = 1


class CustomManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractUser):
    username = None
    phone_number = models.CharField(
        max_length=20, validators=[RegexValidator(r"^\+?1?\d{9,15}$")]
    )
    address = models.TextField()
    is_staff = models.BooleanField(default=False)
    email = models.EmailField(unique=True)

    objects: CustomManager = CustomManager()
    USERNAME_FIELD = "email"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def create_code(self):
        code = "".join([str(random.randint(0, 100) % 10) for i in range(5)])
        VerificationOtp.objects.create(
            user_id=self.id,  # type: ignore
            code=code,
        )
        return code, self.id # type: ignore

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class VerificationOtp(models.Model):
    REGISTER_TYPE = (("register", "register"), ("reset-password", "reset-password"))
    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="codes"
    )
    code = models.IntegerField()
    type = models.CharField(choices=REGISTER_TYPE)
    expiration_time = models.DateTimeField()
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email}"

    class Meta:
        verbose_name = "Verification Otp"
        verbose_name_plural = "Verification Otps"

    def save(self, *args, **kwargs):
        if not self.expiration_time:
            self.expiration_time = timezone.now() + timedelta(minutes=EXPIRATION_TIME)
        super(VerificationOtp, self).save(*args, **kwargs)


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    apartment = models.CharField(max_length=255)
    street = models.TextField()
    pin_code = models.CharField(max_length=255)
    # city

    def __str__(self):
        return f"{self.user} {self.name}"

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
