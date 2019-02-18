from django.core.management import BaseCommand

from stock.models import Equipment


equipments = [
    {
        "id": "1",
        "name": "Коробка A5",
        "geometry": Equipment.Geometries.BOX,
        "width": 200,
        "height": 45,
        "length": 300,
        "weight": 123
    },
    {
        "id": "2",
        "name": "Тубус",
        "geometry": Equipment.Geometries.TUBE,
        "width": 80,
        "height": 80,
        "length": 320,
        "weight": 117
    }
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        for equipment in equipments:
            Equipment.objects.update_or_create(id=equipment["id"], defaults=equipment)

