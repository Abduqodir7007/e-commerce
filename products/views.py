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
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
