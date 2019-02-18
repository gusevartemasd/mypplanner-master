# Generated by Django 2.1.3 on 2018-12-06 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_auto_20181206_1135'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'verbose_name': 'article', 'verbose_name_plural': 'articles'},
        ),
        migrations.AlterField(
            model_name='article',
            name='amo_crm_sku',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='amo_crm_sku'),
        ),
        migrations.AlterField(
            model_name='article',
            name='geometry',
            field=models.CharField(choices=[('BOX', 'BOX'), ('TUBE', 'TUBE')], default='BOX', max_length=16, verbose_name='geometry'),
        ),
        migrations.AlterField(
            model_name='article',
            name='height',
            field=models.IntegerField(verbose_name='height'),
        ),
        migrations.AlterField(
            model_name='article',
            name='length',
            field=models.IntegerField(verbose_name='length'),
        ),
        migrations.AlterField(
            model_name='article',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8, verbose_name='price'),
        ),
        migrations.AlterField(
            model_name='article',
            name='sku',
            field=models.CharField(help_text='sku.help_text', max_length=255, primary_key=True, serialize=False, verbose_name='sku'),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=512, verbose_name='article.title'),
        ),
        migrations.AlterField(
            model_name='article',
            name='weight',
            field=models.IntegerField(verbose_name='weight'),
        ),
        migrations.AlterField(
            model_name='article',
            name='width',
            field=models.IntegerField(verbose_name='width'),
        ),
    ]
