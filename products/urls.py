from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("categories/", CategoryView.as_view()),
    path("products/", ProductsView.as_view()),
    path("colors/", ProductColorView.as_view()),
    path("sizes/", ProductSizeView.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
