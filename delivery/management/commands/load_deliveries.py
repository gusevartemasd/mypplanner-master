from django.core.management import BaseCommand

from delivery.models import Delivery


items = [
    {
        'id': 1,
        'parse_rule': 'Почта России - 200₽ (от 5 до 14 дней) =200',
        'provider': Delivery.Providers.RUSSIAN_POST.value,
        'cost': 200,
    },
    {
        'id': 2,
        'parse_rule': '1 класс Почта России - 350₽ (до 6 рабочих дней) =350',
        'provider': Delivery.Providers.RUSSIAN_POST.value,
        'cost': 350,
    },
    {
        'id': 3,
        'parse_rule': 'СДЭК до склада - 350₽ (до 4-6 рабочих дней) =350',
        'provider': Delivery.Providers.SDEK.value,
        'cost': 350,
    },
    {
        'id': 4,
        'parse_rule': 'СДЭК курьером - 650₽ (до 3-6 рабочих дней) =650',
        'provider': Delivery.Providers.SDEK.value,
        'cost': 650,
    },
    {
        'id': 5,
        'parse_rule': 'СДЭК супер-экспресс до двери - 830₽ (до 2 рабочих дней) =830',
        'provider': Delivery.Providers.SDEK.value,
        'cost': 830,
    },
    {
        'id': 6,
        'parse_rule': 'Страны СНГ и другие страны (Почтой России) - 650₽ =650',
        'provider': Delivery.Providers.RUSSIAN_POST.value,
        'cost': 650,
    },
    {
        'id': 7,
        'parse_rule': 'Самовывоз (Томск, пр. Ленина, д. 30/2, оф. 258, 1 этаж с 11 до 18) =0',
        'provider': Delivery.Providers.PICKUP.value,
        'cost': 0,
    },
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        for item in items:
            Delivery.objects.update_or_create(id=item['id'], defaults=item)
