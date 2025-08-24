from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, DestroyAPIView

from django.http import Http404


class CartAddView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = CartItemsSerializer

    def post(self, request):
        try:
            serializer = CartItemsSerializer(data=request.data)
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
    serializer_class = CartItemUpdateSerializer

    def put(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
            item = CartItem(product=product, user=request.user)
            serializer = CartItemUpdateSerializer(item, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data={"msg": "Updated"})
        except Product.DoesNotExist:
            return Response(data={"msg": "Product does not found"})
        except Exception as e:
            return Response(data={"msg": f"Error: {e}"})


class CartItemsView(ListAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemsSerializer


class DeleteCartItemView(DestroyAPIView):
    serializer_class = CartItemUpdateSerializer

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        try:
            return CartItem.objects.filter(id=pk)
        except CartItem.DoesNotExist:
            raise Http404("Item not found")
