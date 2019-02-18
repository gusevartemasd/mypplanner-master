import requests
import base64
import json

from django.conf import settings
from pymongo import MongoClient

from common import mongolog
from orders.models import Order, Article
from shops.processing.exceptions import ForeignDeliveryException, AddressNormalizationException


def to_base64(st):
    return base64.b64encode(st.encode()).decode('utf-8')


def build_headers():
    access_token = settings.RUSS_POST_TOKEN
    login_password = to_base64(':'.join([settings.RUSS_POST_LOGIN, settings.RUSS_POST_PASSWORD]))
    return {
        'Content-Type': 'application/json;charset=UTF-8',
        'Accept': 'application/json;charset=UTF-8',
        'Authorization': 'AccessToken ' + access_token,
        'X-User-Authorization': 'Basic ' + login_password
    }


def normalize_address(address):
    base_url = settings.RUSS_POST_BASE_URL
    path = '/1.0/clean/address'
    addresses = [
        {
            'id': 'addr',
            'original-address': address
        }
    ]
    url = base_url + path
    response = requests.post(url, headers=build_headers(), data=json.dumps(addresses))
    if response.status_code != 200:
        raise ValueError
    json_data = response.json()[0]
    if json_data['quality-code'] not in ['GOOD', 'POSTAL_BOX', 'ON_DEMAND', 'UNDEF_05']:
        raise ValueError
    if json_data['validation-code'] not in ['VALIDATED', 'OVERRIDDEN', 'CONFIRMED_MANUALLY']:
        raise ValueError
    not_address_fields = ['id', 'original_address', 'quality-code', 'validation-code', 'address-type', 'original-address']
    address_fields = dict()
    for item in json_data:
        if item in not_address_fields:
            continue
        address_fields[item + '-to'] = json_data[item]
    return address_fields


def post(order: Order):
    # properties
    base_url = settings.RUSS_POST_BASE_URL
    path = '/1.0/user/backlog'

    if order.delivery.id == 1:

        # define mail properties
        if order.has_geometry(Article.Geometries.TUBE.value):
            mail_type = 'POSTAL_PARCEL'
            mail_category = 'ORDINARY'
            payment_method = 'CASHLESS'
        else:
            mail_type = 'BANDEROL'
            mail_category = 'ORDERED'
            payment_method = 'STAMP'

        parcel_data = {
                'address-type-to': 'DEFAULT',
                'given-name': order.first_name,
                'middle-name': order.middle_name,
                'surname': order.last_name,
                'recipient-name': order.full_name,
                'sms-notice-recipient': 0,
                'mail-category': mail_category,
                'mail-direct': 643,
                'mail-type': mail_type,
                'payment-method': payment_method,
                'mass': order.weight,
                'order-num': str(order.payment_id),
                # 'postoffice-code': '101000',
                # 'tel-address': order.phone,
                'transport-type': 'AVIA',
                'str-index-to': order.address.postal_code,
                'fragile': False,
                'courier': False,
                'wo-mail-rank': True,
                'manual-address-input': False,
            }

        if mail_type != 'BANDEROL':
            parcel_data['dimension'] = {
                'height': order.height,
                'length': order.length,
                'width': order.width
            }

    elif order.delivery.id == 2:
        # define mail properties
        if order.has_geometry(Article.Geometries.TUBE.value):
            mail_type = 'PARCEL_CLASS_1'
            mail_category = 'ORDINARY'
            payment_method = 'CASHLESS'
        else:
            mail_type = 'BANDEROL_CLASS_1'
            mail_category = 'ORDERED'
            payment_method = 'STAMP'

        parcel_data = {
                'address-type-to': 'DEFAULT',
                'given-name': order.first_name,
                'middle-name': order.middle_name,
                'surname': order.last_name,
                'recipient-name': order.full_name,
                'sms-notice-recipient': 0,
                'mail-category': mail_category,
                'mail-direct': 643,
                'mail-type': mail_type,
                'payment-method': payment_method,
                'mass': order.weight,
                'order-num': str(order.payment_id),
                # 'postoffice-code': '101000',
                # 'tel-address': order.phone,
                'transport-type': 'AVIA',
                'str-index-to': order.address.postal_code,
                'fragile': False,
                'courier': False,
                'wo-mail-rank': True,
                'manual-address-input': False,
            }

        if mail_type != 'BANDEROL_CLASS_1':
            parcel_data['dimension'] = {
                'height': order.height,
                'length': order.length,
                'width': order.width
            }

    elif order.delivery.id == 6:
        # TODO: implement foreign delivery
        raise ForeignDeliveryException(order)

    # get address data
    try:
        parcel_data.update(normalize_address(order.address.result))
    except ValueError:
        raise AddressNormalizationException(order)

    order_data = [parcel_data]

    url = base_url + path
    mongolog.log('delivery', {
        'name': 'russian_post',
        'order_id': order.id,
        'data': order_data,
    })
    response = requests.put(url, headers=build_headers(), data=json.dumps(order_data))
    return response.json()


def request_barcode(shipment_id):
    # properties
    base_url = settings.RUSS_POST_BASE_URL
    path = '/1.0/backlog/%s' % (shipment_id,)

    url = base_url + path
    mongolog.log('delivery', {
        'name': 'russian_post_get_barcode',
        'order_id': shipment_id,
    })
    response = requests.get(url, headers=build_headers())
    status = response.status_code
    data = response.json()
    mongolog.log('delivery', {
        'name': 'russian_post_get_barcode.response',
        'status': response.status_code,
        'data': response.json(),
    })

    if status >= 400:
        raise RuntimeError('Error exec request ' + response.reason)

    return data.get('barcode')
