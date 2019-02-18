import csv
import os

from django.core.management import BaseCommand

from delivery.models import SdekCity

SDEK_CITY_ID = 0
FIAS = 14
KLADR = 15
PVZ_CODE = 17


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('csv', type=str)

    def handle(self, *args, **options):
        csv_file = options['csv']
        if not os.path.exists(csv_file):
            print('File does not exist')
            exit()

        with open(csv_file, newline='') as csv_descriptor:
            reader = csv.reader(csv_descriptor, delimiter=',', quotechar='"', )
            next(reader)
            for row in reader:
                data = dict()
                data["id"] = int(row[SDEK_CITY_ID])
                data["fias"] = row[FIAS]
                data["kladr"] = row[KLADR]
                data["pvz_code"] = row[PVZ_CODE]

                if not data["fias"]:
                    continue

                SdekCity.objects.update_or_create(id=data['id'], defaults=data)
