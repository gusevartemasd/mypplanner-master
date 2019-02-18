import csv

from django.contrib import admin
from articles.models import Article
from django.http import HttpResponse


def export_as_json(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="articles.csv"'

    writer = csv.writer(response)

    fields = Article._meta.fields
    r = list()
    for f in fields:
        r.append(f.verbose_name)
    writer.writerow(r)

    for obj in queryset:
        row = list()
        for field in fields:
            row.append(getattr(obj, field.name))
        writer.writerow(row)

    return response


export_as_json.short_description = "Выгрузить в  CSV"


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    actions = [export_as_json]
    list_display = (
        'title',
        'sku',
        'geometry',
        'price',
    )
