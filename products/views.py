from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated


class CategoryView(ListAPIView):
    permission_classes = [
        IsAuthenticated,
    ]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductsView(ListAPIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = ProductSerializer

    def get_queryset(self):
        min_price = self.request.query_params.get("min_price", None)
        max_price = self.request.query_params.get("max_price", None)
        category = self.request.query_params.get("category", None)
        size_id = self.request.query_params.get("size", None)

        queryset = Product.objects.all()

        if size_id:
            size_id = size_id.split(",")
            queryset = queryset.filter(sizes__id__in=size_id)
        if category:
            category = category.split(",")
            queryset = queryset.filter(category__id__in=category)
        if min_price and max_price:
            queryset = queryset.filter(price__gte=min_price, price__lte=max_price)
        if min_price and not max_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price and not min_price:
            queryset = queryset.filter(price__lte=max_price)
        return queryset


class ProductColorView(ListAPIView):
    queryset = ProductColor.objects.all()
    serializer_class = ColorSerializer


class ProductSizeView(ListAPIView):
    queryset = ProductSize.objects.all()
    serializer_class = SizeSerializer
