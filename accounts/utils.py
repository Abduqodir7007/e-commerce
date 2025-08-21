from django.core.mail import send_mail
from core.settings.base import EMAIL_HOST_USER
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken


def send_email(code, user_email):
    message = f"Your code: {code}"

    send_mail(
        subject="Register code",
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=False,
    )


def create_test_user(
    self,
    email="test@example.com",
    password="easypassword",
    first_name="testname",
    last_name="testlastname",
):
    user = User.objects.create_user(
        email=email, first_name=first_name, last_name=last_name, password=password
    )
    refresh = RefreshToken.for_user(user)
    token = str(refresh.access_token)
    return user, token
