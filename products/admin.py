from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price",
        "category",
    )

    list_filter = ("category",)


class CategoryAdmin(MPTTModelAdmin):
    list_display = ("id", "name", "parent")
    search_fields = ("name",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            kwargs["queryset"] = Category.objects.filter(parent=None).all()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ProductColorAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "color")


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating")
    list_filter = ("rating",)


class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ("id", "value", "product")


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductColor, ProductColorAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(ProductSize, ProductSizeAdmin)
