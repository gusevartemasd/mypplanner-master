# Generated by Django 2.1.3 on 2018-11-19 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20181119_1143'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='height',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='order',
            name='length',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='order',
            name='weight',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='order',
            name='width',
            field=models.IntegerField(default=0),
        ),
    ]
