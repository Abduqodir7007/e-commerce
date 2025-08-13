from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    UserManager,
)
from django.utils.translation import gettext_lazy as _


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
    phone_number = models.CharField(max_length=255)
    address = models.TextField()
    is_staff = models.BooleanField(default=False)

    objects = CustomManager()
    USERNAME_FIELD = "email"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

EXPIRATION_TIME = 2
class VerificationOtp(models.Model):
    REGISTER_TYPE = (
        ('register', 'register'),
        ('password_reset', 'password')
    )
    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="codes"
    )
    code = models.IntegerField()
    type = models.CharField(choices=REGISTER_TYPE,)
    expiration_time = models.DateTimeField()
    
    def __str__(self):
        return f'{self.user.email}'

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    apartment = models.CharField(max_length=255)
    street = models.TextField()
    pin_code = models.CharField(max_length=255)
    # city
    
    def __str__(self):
        return f'{self.user} {self.name}'
    
    
