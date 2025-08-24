from django.http import Http404
from rest_framework.response import Response
from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status

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


class CreateReviewView(APIView):
    serializer_class = CreateReviewSerializer

    def post(self, request):
        try:
            serializer = CreateReviewSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = request.user
            serializer.save(user=user)
            return Response(data={"msg": "Review Created"})
        except Exception as e:
            return Response(data={"msg": f"Error: {e}"})


class ProductReviews(APIView):
     
    def get(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
            reviews = product.review.select_related("user").all()  # type: ignore
            result = []
            for review in reviews:
                result.append(
                    {
                        "user": review.user.full_name,
                        "review": review.review,
                        "rating": review.rating,
                    }
                )

            return Response(data={"msg": "Success", "result": result}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Http404('Product not found')

class GetRelatedProductsView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        try:
            product = Product.objects.get(id=pk)
            return Product.objects.filter(category=product.category).exclude(id=pk)
        except Product.DoesNotExist:
            raise Http404("Item not found")
