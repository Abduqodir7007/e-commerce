import json
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from accounts.models import User
from products.models import ProductReview, Product, Category
from rest_framework_simplejwt.tokens import RefreshToken


def create_product(*args, **kwargs):
    category, _ = Category.objects.get_or_create(name="test category")

    return Product.objects.create(
        name="testname",
        brand="testbrand",
        price="30.0",
        quantity=5,
        category=category,
        short_desciption="test description",
        description="test desciption",
        instruction="test instruction",
    )


def create_user(*args, **kwargs):
    return User.objects.create_user(
        first_name="testuser",
        last_name="testlastname",
        password="password123",
        email="test@gmail.com",
    )



class TestCategoryView(APITestCase):

    def test_happy(self):
        url = reverse("category")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)


class TestProductReviewsView(APITestCase):

    def setUp(self):
        self.user = create_user()
        token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(token.access_token)}")  # type: ignore
        self.product = create_product()
        self.review = ProductReview.objects.create(
            product=self.product, rating=5, user=self.user, review="Good Product"
        )

    def test_happy(self):
        url = reverse("review", args=[self.product.id])  # type: ignore

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["msg"], "Success")  # type: ignore


class TestGetRelatedProductView(APITestCase):
    def setUp(self):
        self.user = create_user()
        token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(token.access_token)}")  # type: ignore
        self.product1 = create_product()
        self.product2 = create_product()
        self.product3 = create_product()
        self.product4 = create_product()

    def test_happy(self):
        url = reverse("related-products", args=[self.product1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
