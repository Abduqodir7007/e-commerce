from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "category",
    )

    list_filter = ("category",)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class ProductColorAdmin(admin.ModelAdmin):
    list_display = ("id",)


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating")
    list_filter = ("rating",)


class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ("value",)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, MPTTModelAdmin, list_display=("name", "parent"))
admin.site.register(ProductColor, ProductColorAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(ProductSize, ProductSizeAdmin)
