from django.contrib import admin
from .models import *


class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "quantity", "subtotal")


class CardAdmin(admin.ModelAdmin):
    list_display = ("card_name", "user")


class DiscountAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "percentage",
        "min_amount",
        "strart_date",
        "end_date",
        "is_active",
    )


class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", "region", "address")


class DeliveryTrafficAdmin(admin.ModelAdmin):
    list_display = ("delivery_time", "price")


class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "total_amount", "status")


admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(DeliveryTraffice, DeliveryTrafficAdmin)
admin.site.register(Order, OrderAdmin)
