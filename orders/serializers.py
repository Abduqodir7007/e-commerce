from rest_framework import serializers
from products.serializers import ProductSerializer

class CartItemUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(required=True)

    def update(self, instance, validated_data):
        quantity = validated_data.get("quantity")
        instance.quantity = quantity
        instance.save()
        return instance



class CartItemsSerializer(serializers.Serializer):
    product = ProductSerializer(read_only=True)
    quantity = serializers.IntegerField()
    subtotal = serializers.FloatField()