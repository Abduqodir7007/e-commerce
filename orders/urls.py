from django.urls import path
from .views import *

urlpatterns = [
    path("", OrderListView.as_view()),
    path("add-to-cart/", CartAddView.as_view()),
    path("cart-items/", CartItemsView.as_view()),
    path("cart-item/<str:pk>/", UpdataCartView.as_view()),
    path("cart-item/<str:pk>/delete/", DeleteCartItemView.as_view()),
    path("create/", OrderCreateView.as_view()),
    path("order-cancel/<str:pk>/", DeleteOrderView.as_view()),
    path("order-update/<str:pk>/", OrderUpdateView.as_view()),
]
