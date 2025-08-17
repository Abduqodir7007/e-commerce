from django.core.mail import send_mail
from core.settings.base import EMAIL_HOST_USER
from datetime import datetime
from rest_framework.exceptions import ValidationError
def send_email(code, user_email):
    message = f"Your code: {code}"

    send_mail(
        subject="Register code",
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=False,
    )



