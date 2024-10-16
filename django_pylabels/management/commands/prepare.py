from django.core.exceptions import ObjectDoesNotExist
from django.core.management import BaseCommand

from django_pylabels.models import LabelSpecification


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            LabelSpecification.objects.get(name="default")
        except ObjectDoesNotExist:
            LabelSpecification.objects.create()
            print("Created default label specification.")
        else:
            print("Default label specification already exists.")
        print("Created a default user `admin` with password `admin`")
