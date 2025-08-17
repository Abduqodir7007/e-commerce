from django.urls import path
from .views import *


urlpatterns = [
    path("register/", CreateUser.as_view()),
    path("verify/", VerifyView.as_view()),
    path('reset-password/', ResetPassword.as_view()),
    path('login/', LoginView.as_view()),
]
