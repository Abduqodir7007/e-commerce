from rest_framework import serializers
from .models import *
from django.conf import settings


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = "__all__"

    def get_file(self, obj):
        return str(settings.HOST) + str(obj.file.url)
