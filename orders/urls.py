from django.urls import path
from .views import *

urlpatterns = [
    path("add-cart/", CartView.as_view()),
    path("update-cart/<str:pk>/", UpdataCartView.as_view()),
]
