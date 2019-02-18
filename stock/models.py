from django.db import models
from django.utils.translation import gettext_lazy as _

from common import ChoiceEnum


class Equipment(models.Model):
    class Geometries(ChoiceEnum):
        BOX = 'BOX'
        TUBE = 'TUBE'

    name = models.CharField(verbose_name=_('name'), max_length=128)
    geometry = models.CharField(verbose_name=_('geometry'), max_length=32, choices=Geometries.choices())
    width = models.IntegerField(verbose_name=_('width'))
    height = models.IntegerField(verbose_name=_('height'))
    length = models.IntegerField(verbose_name=_('length'))
    weight = models.IntegerField(verbose_name=_('weight'))

    def __str__(self):
        return '%s (%s)' % (self.name, self.geometry)

    class Meta:
        verbose_name = _('equipment')
        verbose_name_plural = _('equipments')
