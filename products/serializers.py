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
            "category",
            "in_stock",
            "thumbnail",
        )


class ColorSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    color = MediaSerializer(read_only=True)


class SizeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    value = serializers.CharField()


class CreateReviewSerializer(serializers.Serializer):
    review = serializers.CharField(required=True)
    rating = serializers.IntegerField(required=True)
    product_id = serializers.IntegerField(required=True)

    def validate_rating(self, value):
        if value < 0 and value > 5:
            raise ValidationError("Invalid rate")
        return value

    def create(self, validated_data):
        return ProductReview.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.review = validated_data.get("review", None)
        instance.rating = validated_data.get("rating", None)
        instance.product = Product.objects.get(id=validated_data.get("product_id"))
        instance.save()
        return instance

class ProductReviewSerializer(serializers.Serializer):
    review = serializers.CharField()
    rating = serializers.IntegerField()
    product_id = serializers.IntegerField()