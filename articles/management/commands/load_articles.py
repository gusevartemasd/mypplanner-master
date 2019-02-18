from django.core.management import BaseCommand

from articles.models import Article


articles = [
    {
        'sku': '123456789',
        'title': 'Ежедневник Творю жизнь',
        'geometry': Article.Geometries.BOX.value,
        'width': 200,
        'height': 10,
        'length': 300,
        'price': 890,
        'weight': 50,
    },
    {
        'sku': '12345678',
        'title': 'Ежедневник Выбирай путь',
        'geometry': Article.Geometries.BOX.value,
        'width': 200,
        'height': 10,
        'length': 300,
        'price': 800,
        'weight': 55,
    }
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        for article in articles:
            Article.objects.update_or_create(sku=article['sku'], defaults=article)
