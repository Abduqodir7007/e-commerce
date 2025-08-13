from django.db import models
from common.models import Media
from django_ckeditor_5.fields import CKEditor5Field
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ForeignKey(Media, on_delete=models.SET_NULL, null=True, blank=True)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    short_desciption = models.TextField()
    description = models.TextField()
    quantity = models.IntegerField()
    instruction = CKEditor5Field('Text', config_name='awesome_ckeditor')