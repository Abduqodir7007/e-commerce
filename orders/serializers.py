from rest_framework import serializers


class CartSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(required=True)

    def update(self, instance, validated_data):
        quantity = validated_data.get("quantity")
        instance.quantity = quantity
        instance.save()
        return instance



