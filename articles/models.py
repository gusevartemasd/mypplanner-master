from django.db import models
from django.utils.translation import ugettext_lazy as _

from common import ChoiceEnum


def build_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '.'.join([str(instance.pk), ext])
    return 'articles/{filename}'.format(filename=filename)


class Article(models.Model):
    class Geometries(ChoiceEnum):
        BOX = 'BOX'
        TUBE = 'TUBE'

    sku = models.CharField(
        verbose_name=_('sku'),
        help_text=_('sku.help_text'),
        max_length=255,
        primary_key=True,
    )
    title = models.CharField(
        verbose_name=_('article.title'),
        max_length=512,
    )
    geometry = models.CharField(
        verbose_name=_('geometry'),
        choices=Geometries.choices(),
        max_length=16,
        default=Geometries.BOX.value,
    )
    width = models.IntegerField(
        verbose_name=_('width'),
    )
    height = models.IntegerField(
        verbose_name=_('height'),
    )
    length = models.IntegerField(
        verbose_name=_('length'),
    )
    price = models.DecimalField(
        verbose_name=_('price'),
        decimal_places=2,
        max_digits=8,
    )
    weight = models.IntegerField(
        verbose_name=_('weight'),
    )
    amo_crm_sku = models.CharField(
        verbose_name=_('amo_crm_sku'),
        max_length=255,
        null=True,
        blank=True
    )

    def __str__(self):
        return '%s (%s)' % (self.title, self.price)

    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('articles')
