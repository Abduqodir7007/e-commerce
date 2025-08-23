from django.urls import path
from .views import *

urlpatterns = [
    path("add-to-cart/", CartAddView.as_view()),
    path("cart-items/", CartItemsView.as_view()),
    path("cart-item/<str:pk>/", UpdataCartView.as_view()),
    path("cart-item/<str:pk>/delete/", DeleteCartItemView.as_view()),
]
