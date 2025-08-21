from django.contrib import admin
from .models import *


class MediaAdmin(admin.ModelAdmin):
    list_display = ("id",)


admin.site.register(Media, MediaAdmin)
admin.site.register(Settings)
admin.site.register(Country)
admin.site.register(Region)
admin.site.register(InstagramStory)
admin.site.register(CustomerFeedback)
