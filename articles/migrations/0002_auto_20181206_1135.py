# Generated by Django 2.1.3 on 2018-12-06 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'verbose_name': 'артикул', 'verbose_name_plural': 'артикулы'},
        ),
        migrations.AddField(
            model_name='article',
            name='amo_crm_sku',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='артикул в AmoCRM'),
        ),
        migrations.AlterField(
            model_name='article',
            name='geometry',
            field=models.CharField(choices=[('BOX', 'BOX'), ('TUBE', 'TUBE')], default='BOX', max_length=16, verbose_name='геометрия'),
        ),
        migrations.AlterField(
            model_name='article',
            name='height',
            field=models.IntegerField(verbose_name='высота'),
        ),
        migrations.AlterField(
            model_name='article',
            name='length',
            field=models.IntegerField(verbose_name='длина'),
        ),
        migrations.AlterField(
            model_name='article',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8, verbose_name='цена'),
        ),
        migrations.AlterField(
            model_name='article',
            name='sku',
            field=models.CharField(help_text='sku.help_text', max_length=255, primary_key=True, serialize=False, verbose_name='артикул'),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=512, verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='article',
            name='weight',
            field=models.IntegerField(verbose_name='вес'),
        ),
        migrations.AlterField(
            model_name='article',
            name='width',
            field=models.IntegerField(verbose_name='ширина'),
        ),
    ]
