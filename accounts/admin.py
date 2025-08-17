from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "phone_number")
    list_filter = ("email", "id")


class VerificationOtpAdmin(admin.ModelAdmin):
    list_display = ("id","user", "type")


class AddressAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name")


admin.site.register(VerificationOtp, VerificationOtpAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Address, AddressAdmin)
