from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from accounts.models import User
from products.models import ProductReview, Product, Category
from rest_framework_simplejwt.tokens import RefreshToken


class TestCategoryView(APITestCase):

    def test_happy(self):
        url = reverse("category")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)


class TestProductReviewsView(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            first_name="testuser",
            last_name="testlastname",
            password="password123",
            email="test@gmmail.com",
        )
        token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")  # type: ignore

        self.category = Category.objects.create(name="test category")
        self.product = Product.objects.create(
            name="testname",
            brand="testbrand",
            price="30.0",
            quantity=5,
            category=self.category,
            short_desciption="test description",
            description="test desciption",
            instruction="test instruction",
        )
        self.review = ProductReview.objects.create(
            product=self.product, rating=5, user=self.user, review="Good Product"
        )
        self.url = reverse("review", args=[self.product.id])  # type: ignore

    def test_happy(self):
        url = reverse("review", args=[self.product.id])  # type: ignore

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["msg"], "Success")  # type: ignore


