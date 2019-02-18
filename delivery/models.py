from django.db import models

from common import ChoiceEnum


class Delivery(models.Model):
    class Providers(ChoiceEnum):
        RUSSIAN_POST = 'RUSSIAN_POST'
        SDEK = 'SDEK'
        PICKUP = 'PICKUP'

    parse_rule = models.CharField("Строка из Тильды", max_length=500, unique=True)
    provider = models.CharField("служба", max_length=32, choices=Providers.choices())
    cost = models.DecimalField("стоимость", decimal_places=2, max_digits=8)

    def __str__(self):
        return self.parse_rule

    class Meta:
        verbose_name = 'доставка'
        verbose_name_plural = 'доставки'


class SdekCity(models.Model):
    id = models.IntegerField(primary_key=True)
    fias = models.UUIDField()
    kladr = models.CharField(max_length=16)
    pvz_code = models.CharField(max_length=8)

    def __str__(self):
        return self.pvz_code
