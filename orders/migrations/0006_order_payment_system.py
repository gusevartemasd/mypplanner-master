# Generated by Django 2.1.3 on 2018-11-22 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_orderaddress_unparsed_parts'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_system',
            field=models.CharField(blank=True, default=None, max_length=63, null=True),
        ),
    ]
