from django.contrib import admin

from stock.models import Equipment


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'geometry',
        'width',
        'height',
        'length'
    )
