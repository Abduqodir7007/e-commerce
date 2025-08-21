from celery import shared_task
from django.core.mail import send_mail
from core.settings.base import EMAIL_HOST_USER


@shared_task
def send_otp_code_to_email(code, email):
    message = f"Your code: {code}"

    send_mail(
        subject="Register code",
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )
