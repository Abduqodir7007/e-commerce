from django.db import models
from common.models import Media
from django_ckeditor_5.fields import CKEditor5Field
from common.models import Media
from accounts.models import User
from mptt.models import MPTTModel, TreeForeignKey
from rest_framework.exceptions import ValidationError


def discount_validator(x):
    if x > 100:
        raise ValidationError({"msg": "too high"})


class Category(MPTTModel):
    name = models.CharField(max_length=255)
    image = models.ForeignKey(Media, on_delete=models.SET_NULL, null=True, blank=True)
    parent = TreeForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    brand = models.CharField(max_length=255, help_text="Brand Name")
    name = models.CharField(max_length=255)
    price = models.FloatField()
    short_desciption = models.TextField()
    description = models.TextField()
    quantity = models.IntegerField()
    in_stock = models.BooleanField(default=False)
    instruction = CKEditor5Field("Text", config_name="awesome_ckeditor")
    # image = models.ForeignKey(Media, on_delete=models.CASCADE)
    discount = models.IntegerField(
        help_text="discount in percentage",
        validators=[discount_validator],
        null=True,
        blank=True,
    )
    thumbnail = models.ForeignKey(
        Media,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="thumbnail",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
    )


class ProductColor(models.Model):
    color = models.ForeignKey(Media, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="color")

    def __str__(self):
        return f"{self.product.name}"

    class Meta:
        verbose_name = "Product Color"
        verbose_name_plural = "Product Colors"


class ProductSize(models.Model):
    value = models.CharField(max_length=10)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Product Size"
        verbose_name_plural = "Product Sizes"


class ProductReview(models.Model):
    review = models.TextField()
    rating = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )

    def __str__(self) -> str:
        return f"{self.product.name}" + "review"

    class Meta:
        verbose_name = "Product Review"
        verbose_name_plural = "Product Reviews"
