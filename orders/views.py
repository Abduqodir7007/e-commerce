from rest_framework import status
from .models import *
from .serializers import *
from accounts.permissions import IsOwner
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from datetime import datetime
from rest_framework.generics import (
    ListAPIView,
    DestroyAPIView,
    CreateAPIView,
    UpdateAPIView,
)

from django.http import Http404


class CartAddView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = CartItemAddUpdateSerializer

    def post(self, request):
        try:
            serializer = CartItemAddUpdateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            product = Product.objects.get(id=data.get("id"))
            if CartItem.objects.filter(product=product, user=request.user).exists():
                return Response(data={"msg": "Already added"})

            item = CartItem.objects.create(
                user=request.user, quantity=data.get("quantity"), product=product
            )

            return Response(
                data={"msg": "Cart item added"}, status=status.HTTP_201_CREATED
            )
        except Product.DoesNotExist:
            return Response(
                data={"msg": "Product does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UpdataCartView(APIView):
    serializer_class = CartItemAddUpdateSerializer

    def put(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
            item = CartItem(product=product, user=request.user)
            serializer = CartItemAddUpdateSerializer(
                item, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data={"msg": "Updated"})
        except Product.DoesNotExist:
            return Response(data={"msg": "Product does not found"})
        except Exception as e:
            return Response(data={"msg": f"Error: {e}"})


class CartItemsView(ListAPIView):
    serializer_class = CartItemsSerializer

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)


class DeleteCartItemView(DestroyAPIView):
    serializer_class = CartItemAddUpdateSerializer

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        try:
            return CartItem.objects.filter(id=pk)
        except CartItem.DoesNotExist:
            raise Http404("Item not found")


class OrderCreateView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = OrderCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            #payment = serializer.validated_data.get('payment')
            items = CartItem.objects.filter(
                id__in=serializer.validated_data.get("item")
            )
            if not items.exists():
                return Response(data={"msg": "Product not found"})

            total_amount = sum([item.subtotal for item in items])
            address = Address.objects.get(id=serializer.validated_data.get("address"))

            order = Order.objects.create(
                user=request.user, address=address, total_amount=total_amount
            )
            order.items.set(items)
            order.save()
            return Response(data={"msg": "Created"})
        except Exception as e:
            return Response(data={"msg": e})


class OrderListView(ListAPIView):
    serializer_class = OrderListSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class DeleteOrderView(DestroyAPIView):
    permission_classes = [IsOwner]
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    lookup_field = "pk"


class OrderDiscountView(APIView):
    serializer_class = OrderDiscountSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            order = Order.objects.get(id=serializer.validated_data.get("order_id"))
            discount = Discount.objects.get(
                code=serializer.validated_data.get("discount_code"),
                is_active=True,
                end_date__gte=datetime.now(),
            )
            if order.total_amount < int(discount.min_amount):
                return Response(data={"msg": "You cannot apply this discount"})
            order.total_amount = order.total_amount * (1 - discount.percentage / 100)
            order.discount = discount
            order.save()
            return Response(data={"msg": "Discount applied"})
        except Discount.DoesNotExist:
            return Response(data={"msg": "Wrong discount code"})
        except Order.DoesNotExist:
            return Response(data={"msg": "Order does not exist"})


# class OrderUpdateView(UpdateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderUpdateSerializer
#     lookup_field = "pk"
