from common.models import *
from django.core.management.base import BaseCommand
import json


class Command(BaseCommand):
    help = "Load all regions"

    def handle(self, *args, **options):
        with open(
            "D:/tutorials/projects/real/e-commerce/data/regions.json", "r"
        ) as file:
            regions = json.load(file)
            country = Country.objects.get(name="Uzbekistan")

            for reg in regions:
                Region.objects.get_or_create(name=reg['name_uz'], country=country)

        self.stdout.write(self.style.SUCCESS("loaded all regions"))
