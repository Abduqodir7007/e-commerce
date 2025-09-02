from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from products.tests import create_product, create_user
from accounts.models import Address
from .models import Order


class TestOrderCreateView(APITestCase):
    def setUp(self) -> None:
        self.user = create_user()
        self.product1 = create_product()
        self.product2 = create_product()
        self.address = Address.objects.create(
            user=self.user,
            name="test address",
            phone_number=901001223,
            apartment="test apartent",
            street="test",
            pin_code="1234",
        )
        self.order = Order.objects.create(
            user=self.user, payment_method="cash", address=self.address
        )
        

    def test_happy(self):
        url = reverse("order")
        data = {"item": [1,2], "address":1, "payment": "cash"}
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)