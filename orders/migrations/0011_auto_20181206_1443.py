# Generated by Django 2.1.3 on 2018-12-06 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_auto_20181206_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_id',
            field=models.CharField(max_length=15, unique=True, verbose_name='номер платежа'),
        ),
    ]