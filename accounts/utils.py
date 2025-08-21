from .models import *
from rest_framework_simplejwt.tokens import RefreshToken



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
