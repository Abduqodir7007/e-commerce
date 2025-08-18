from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.generics import ListAPIView

class CategoryView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    
class ProductsView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    