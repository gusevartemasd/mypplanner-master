from django.db import models
from django.utils.translation import gettext_lazy as _
from articles.models import Article
from delivery.models import Delivery
from stock.models import Equipment


class OrderAddress(models.Model):
    source = models.CharField(max_length=512, null=True, blank=True)
    result = models.CharField(max_length=511, null=True, blank=True)
    postal_code = models.CharField(max_length=6, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)
    region_fias_id = models.UUIDField(null=True, blank=True)
    region_type = models.CharField(max_length=5, null=True, blank=True)
    area = models.CharField(max_length=255, null=True, blank=True)
    area_fias_id = models.UUIDField(null=True, blank=True)
    area_type = models.CharField(max_length=5, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    city_fias_id = models.UUIDField(null=True, blank=True)
    city_type = models.CharField(max_length=5, null=True, blank=True)
    city_district = models.CharField(max_length=255, null=True, blank=True)
    city_district_fias_id = models.UUIDField(null=True, blank=True)
    city_district_type = models.CharField(max_length=5, null=True, blank=True)
    settlement = models.CharField(max_length=255, null=True, blank=True)
    settlement_fias_id = models.UUIDField(null=True, blank=True)
    settlement_type = models.CharField(max_length=5, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    street_fias_id = models.UUIDField(null=True, blank=True)
    street_type = models.CharField(max_length=5, null=True, blank=True)
    house = models.CharField(max_length=255, null=True, blank=True)
    house_fias_id = models.UUIDField(null=True, blank=True)
    house_type = models.CharField(max_length=5, null=True, blank=True)
    block = models.CharField(max_length=64, null=True, blank=True)
    block_type = models.CharField(max_length=5, null=True, blank=True)
    flat = models.CharField(max_length=64, null=True, blank=True)
    flat_type = models.CharField(max_length=5, null=True, blank=True)
    geo_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    geo_lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    unparsed_parts = models.CharField(max_length=255, null=True, blank=True, default=None)

    def __str__(self):
        return self.result


class Order(models.Model):
    payment_id = models.CharField(verbose_name=_('payment_id'), max_length=15, unique=True)
    amo_order_id = models.CharField(max_length=32, unique=True, null=True, blank=True)
    full_name = models.CharField(verbose_name=_('full_name'), max_length=511)
    first_name = models.CharField(verbose_name=_('first_name'), max_length=63, null=True, blank=True)
    middle_name = models.CharField(verbose_name=_('middle_name'), max_length=63, null=True, blank=True)
    last_name = models.CharField(verbose_name=_('last_name'), max_length=63, null=True, blank=True)
    phone = models.CharField(verbose_name=_('phone'), max_length=31)
    email = models.EmailField(verbose_name=_('email'), max_length=255)
    delivery = models.ForeignKey(Delivery, verbose_name=_('delivery'), null=True, on_delete=models.DO_NOTHING)
    address = models.OneToOneField(OrderAddress, verbose_name=_('address'), on_delete=models.DO_NOTHING)
    #address = models.TextField(verbose_name=_('address'), default="", blank=True, null=True)
    comment = models.TextField(verbose_name=_('comment'), default="", blank=True, null=True)
    weight = models.IntegerField(verbose_name=_('weight'), default=0)
    height = models.IntegerField(verbose_name=_('height'), default=0)
    width = models.IntegerField(verbose_name=_('width'), default=0)
    length = models.IntegerField(verbose_name=_('length'), default=0)
    is_payed = models.BooleanField(verbose_name=_('is_payed'), default=False)
    payment_system = models.CharField(verbose_name=_('payment_system'), max_length=63, default=None, null=True, blank=True)
    promo_code = models.CharField(verbose_name=_('promo_code'), max_length=63, default=None, null=True, blank=True)
    total = models.DecimalField(verbose_name=_('total'), decimal_places=2, max_digits=8)
    track = models.CharField(verbose_name=_('track'), max_length=32, default=None, null=True, blank=True)
    utm_source = models.CharField(max_length=255, default="", blank=True)
    utm_content = models.CharField(max_length=255, default="", blank=True)
    utm_medium = models.CharField(max_length=255, default="", blank=True)
    utm_term = models.CharField(max_length=255, default="", blank=True)
    utm_campaign = models.CharField(max_length=255, default="", blank=True)
    created_at = models.DateTimeField(verbose_name=_('created_at'), auto_now_add=True)

    def __str__(self):
        return self.payment_id

    def has_geometry(self, geometry):
        return self.orderarticle_set.filter(article__geometry=geometry).exists()

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')


class OrderArticle(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.DO_NOTHING)
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return '%s (%s)' % (self.order.id, self.article.title)

    class Meta:
        verbose_name = 'order_article'
        verbose_name_plural = 'order_articles'


class OrderEquipment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.DO_NOTHING)
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return '%s (%s)' % (self.order.id, self.equipment.name)

    class Meta:
        verbose_name = 'order_equipment'
        verbose_name_plural = 'order_equipments'
