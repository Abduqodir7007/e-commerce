from django.db import models
from accounts.models import User, Address
from products.models import Product
from common.models import Region
from datetime import datetime


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.product.price
        super().save(*args, **kwargs)


class Card(models.Model):
    card_name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=16)
    expiry_date = models.DateField()
    cvv = models.CharField(max_length=3)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cards")


class Discount(models.Model):
    min_amount = models.CharField(help_text="Minimum amount for discount to apply")
    code = models.CharField(max_length=50, unique=True)
    percentage = models.IntegerField(help_text="Discount percentage")
    strart_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.is_active = False if datetime.now() > self.end_date else True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.code


class Branch(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE, related_name="branches"
    )
    address = models.CharField(max_length=255)
    longtitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


class DeliveryTraffice(models.Model):
    weight = models.FloatField(help_text="In kilogram")
    delivery_time = models.DurationField(help_text="in hours")
    price = models.FloatField()
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name="delivery_traffic"
    )
    regions = models.ManyToManyField(Region, related_name="delivery_traffics")

    def __str__(self):
        return f"Delivery Traffic for {self.branch.name} - {self.delivery_time}"


class Order(models.Model):
    STATUS = (
        ("created", "created"),
        ("in_progress", "in_progress"),
        ("delivered", "delivered"),
        ("cancelled", "cancelled"),
        ("finished", "finished"),
    )

    PAYMENT_METHODS = (
        ("payme", "payme"),
        ("cash", "cash"),
        ("click", "click"),
    )
    PAYMENT_STATUS = (
        ("paid", "paid"),
        ("pending", "pending"),
        ("cancelled", "cancelled"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    items = models.ManyToManyField(CartItem, related_name="orders")
    total_amount = models.FloatField()
    is_paid = models.BooleanField(default=False)
    status = models.CharField(choices=STATUS, default="created")
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHODS, null=True, blank=True
    )
    payment_status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS, default="pending"
    )
    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, related_name="orders"
    )
    delivery_traffic = models.ForeignKey(
        DeliveryTraffice,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )

    def __str__(self):
        return f"Order by {self.user.username}"
