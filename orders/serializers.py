from rest_framework import serializers
from products.serializers import ProductSerializer
from .models import *
from accounts.serializers import AddressSerializer


class CartItemAddUpdateSerializer(serializers.Serializer):
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
    subtotal = serializers.FloatField(read_only=True)


class OrderCreateSerializer(serializers.Serializer):
    item = serializers.ListField(child=serializers.IntegerField())
    address = serializers.IntegerField(required=True)


class OrderUpdateSerializer(serializers.Serializer):
    items = serializers.ListField(child=serializers.IntegerField())
    address = AddressSerializer(required=False)

    def update(self, instance, validated_data):  # TO DO: update enpoint is now working
        address_id = validated_data.get("address", instance.address.id)

        if "item" in validated_data:  # request provided new items (even empty [])
            item_ids = validated_data["item"]
        else:  # keep existing items
            item_ids = list(instance.items.values_list("id", flat=True))

        address = Address.objects.get(id=address_id)
        items = CartItem.objects.filter(id__in=item_ids)

        instance.address = address
        instance.save()
        return instance

        instance.items.set(items)


class OrderListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    items = CartItemsSerializer(many=True)
    total_amount = serializers.FloatField()
    is_paid = serializers.BooleanField()
    address = AddressSerializer(read_only=True)
