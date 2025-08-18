from rest_framework import serializers
from .models import *
from common.serializers import MediaSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "parent")


class ProductSerializer(serializers.ModelSerializer):
    thumbnail = MediaSerializer(read_only=True)
    class Meta:
        model = Product
        fields = (
            "brand",
            "name",
            "price",
            "image",
            "category",
            "is_stock",
            "thumbnail",
        )
