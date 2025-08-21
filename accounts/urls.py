from django.urls import path
from .views import *


urlpatterns = [
    path("register/", CreateUser.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("verify/", VerifyView.as_view(), name="verify"),
    path("reset-password/start/", ResetPassword.as_view(), name="reset-password1"),
    path(
        "reset-password/finish/", ResetPasswordFinish.as_view(), name="reset-password2"
    ),
    path("get-newcode/", GetNewCodeView.as_view(), name="new_code"),
]
