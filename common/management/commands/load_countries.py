from common.models import *
from django.core.management.base import BaseCommand
import json


class Command(BaseCommand):
    help = "Load all countries"

    def handle(self, *args, **options):
        with open(
            "D:/tutorials/projects/real/e-commerce/data/countries.json", "r"
        ) as file:
            countries = json.load(file)
            
            for country in countries:
                Country.objects.get_or_create(name=country['name'])

        self.stdout.write(self.style.SUCCESS("loaded all countries"))
