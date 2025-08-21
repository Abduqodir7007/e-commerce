from rest_framework_simplejwt.tokens import RefreshToken
from .utils import create_test_user
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import *


class TestUserCreateView(APITestCase):
    def setUp(self) -> None:
        pass

    def test_happy(self):
        url = reverse("register")
        data = {
            "first_name": "testname",
            "last_name": "testlastname",
            "email": "test@gmail.com",
            "password": "easypassword",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(list(response.data.keys()), ["refresh", "access"])  # type: ignore


class TestVerifyView(APITestCase):
    def setUp(self) -> None:
        self.new_user = User.objects.create_user(
            first_name="testname",
            last_name="testlastname",
            email="test@gmail.com",
            password="easypassword",
        )
        self.otp = VerificationOtp.objects.create(
            user=self.new_user, code="12345", type="register"
        )
        token = RefreshToken.for_user(self.new_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")  # type: ignore

    def test_happy(self):
        url = reverse("verify")
        data = {"code": "12345", "verify_type": "register"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.data.keys()), ["success", "access", "refresh"])  # type: ignore
        self.assertEqual(response.data["success"], True)  # type: ignore

    def test_invalid_otp(self):
        url = reverse("verify")
        data = {"code": "21345", "verify_type": "register"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["msg"], "Invalid code")  # type: ignore


class TestLoginView(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name="testname",
            last_name="testlastname",
            email="test@gmail.com",
            password="easypassword",
        )
        token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")  # type: ignore

    def test_happy(self):
        url = reverse("login")
        data = {"email": "test@gmail.com", "password": "easypassword"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.data.keys()), ["refresh", "access"])  # type: ignore

    def test_wrong_email(self):
        url = reverse("login")
        data = {"email": "test@gmail.com", "password": "easypassword1"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

class TestGetNewCodeView(APITestCase):
    pass