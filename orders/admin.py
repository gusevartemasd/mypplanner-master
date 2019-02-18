from django.contrib import admin

from orders.models import Order
from orders.models import OrderAddress
from orders.models import OrderArticle
from orders.models import OrderEquipment


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass

@admin.register(OrderAddress)
class OrderAddressAdmin(admin.ModelAdmin):
    pass

@admin.register(OrderArticle)
class OrderArticleAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderEquipment)
class OrderEquipmentAdmin(admin.ModelAdmin):
    pass

