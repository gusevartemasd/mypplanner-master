import hashlib
from datetime import datetime

import requests
from django.conf import settings
from django.template.loader import get_template

from common import mongolog
from delivery.models import SdekCity
from orders.models import Order, OrderAddress


def build_secure_hash(dt):
    secure = '&'.join([dt, settings.SDEK_SECURE_PASSWORD])
    m = hashlib.md5()
    m.update(secure.encode())
    return m.digest().hex()


def get_rec_city(order_address: OrderAddress):
    # order of fields is important from small village to big city
    fias_fields = [
        'settlement_fias_id',
        'city_district_fias_id',
        'city_fias_id',
        'area_fias_id',
        'region_fias_id'
    ]
    sdek_city = None
    for field in fias_fields:
        fias = getattr(order_address, field)
        if not fias:
            continue
        try:
            sdek_city = SdekCity.objects.get(fias=fias)
            break
        except SdekCity.DoesNotExist:
            continue
    return sdek_city


def get_rec_city_code(order):
    return 1


def get_rec_city_post_code(order):
    return order.address.postal_code


def get_pvz_code(order):
    return 1


def post(order: Order):
    url = 'https://integration.cdek.ru/new_orders.php'
    date_first = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    delivery_data = {
        'secure': build_secure_hash(date_first),
        'account': settings.SDEK_ACCOUNT,
        'order': order,
        'date_first': date_first,
        'send_city_code': 1,
        'rec_city_code': get_rec_city_code(order),
        'send_city_post_code': '123123',
        'rec_city_post_code': get_rec_city_post_code(order),
        'street': order.address.street,
        'house': order.address.house,
        'flat': order.address.flat,
        'pvz_code': get_pvz_code(order),
        'height': order.height/10,
        'width': order.width/10,
        'length': order.length/10,
        'items': order.orderarticle_set.all(),
    }

    xml = get_template('delivery/sdek/delivery.xml').render(delivery_data)
    xml = str(xml).encode('utf-8')

    response = requests.post(url, data={'xml_request': xml})
    data = response.text
    mongolog.log('sdek', {
        'response': data
    })
