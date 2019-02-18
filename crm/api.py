from urllib.parse import urlencode
from jq import jq
import requests
from django.conf import settings

from common import mongolog
from orders.models import Order

DEFAULT_RESPONSIBLE_USER_ID = 2117545
DEFAULT_PIPELINE_ID = 1471219
DEFAULT_STATUS_ID = 22740238


def authorize():
    url = 'https://%s.amocrm.ru/private/api/auth.php?type=json' % settings.AMOCRM_SUBDOMAIN
    data = {
        'USER_LOGIN': settings.AMOCRM_LOGIN,
        'USER_HASH': settings.AMOCRM_HASH
    }
    resp = requests.post(url, data=data)
    if resp.status_code == 200:
        return resp.headers['Set-Cookie']
    return None


def amo_cf(field, value, enum=None):
    cf = {
            'id': field,
            'values': [
                {
                    'value': value
                }
            ]
        }
    if enum:
        cf['values'][0]['enum'] = enum

    return cf


def exec(method, path, query=None, data=None):
    query = query or dict()
    data = data or dict()
    base_query = {'type': 'json'}
    base_query.update(query)
    url = 'https://%s.amocrm.ru/api/v2/%s?%s' % (settings.AMOCRM_SUBDOMAIN, path, urlencode(base_query))

    headers = {'Cookie': authorize(),
               'Content-Type': 'application/json'}

    mongolog.log('crm', {
        'path': path,
        'query': query,
        'data': data,
        'headers': headers,
    })

    if method == 'get':
        resp = requests.get(url, headers=headers)
    elif method == 'post':
        resp =requests.post(url, json=data, headers=headers)
    elif method == 'put':
        resp = requests.put(url, json=data, headers=headers)
    else:
        raise ValueError

    # mongolog.log('crm', {
    #     'status_code': resp.status_code,
    #     'json': resp.json(),
    # })

    return resp


def create_order(order: Order, status=None):
    contact_id = get_or_create_contact(order)
    data = {'add': [{
        'name': 'Заказ',
        'pipeline_id': DEFAULT_PIPELINE_ID,
        'status_id': DEFAULT_STATUS_ID,
        'responsible_user_id': DEFAULT_RESPONSIBLE_USER_ID,
        'sale': str(order.total + order.delivery.cost),
        'tags': "tilda, testing-microservice",
        'contacts_id': [contact_id],
        'custom_fields': [
            amo_cf(577387, order.address.postal_code),
            amo_cf(573607, str(order.total + order.delivery.cost)),
            amo_cf(573609, order.delivery.parse_rule),
            amo_cf(572905, str(order.total)),
            amo_cf(560063, order.payment_id),
            amo_cf(560061, order.payment_system),
            amo_cf(560057, order.address.result if order.address.result is not None else order.address.source),
            amo_cf(560059, order.delivery.parse_rule),
            amo_cf(560065, ';'.join(['%s (кол-во %s)' % (o.article.title, o.quantity) for o in order.orderarticle_set.all()])),
            amo_cf(572901, order.promo_code),
            amo_cf(572763, order.comment)
        ]
    }]}

    if status:
        data['add'][0]['custom_fields'].append(amo_cf(577729, status))

    if order.track:
        data['add'][0]['custom_fields'].append(amo_cf(572620, order.track))

    resp = exec('post', 'leads', data=data)
    if resp.status_code == 200:
        data = resp.json()
        return jq('._embedded.items[0].id').transform(data)
    else:
        return None


def get_or_create_contact(order: Order):
    contact_id = get_contact_by_email(order.email)
    if contact_id is None:
        contact_id = create_contact(order)
    return contact_id


def create_contact(order: Order):
    data = {'add': [
        {
            'name': order.full_name,
            'responsible_user_id': 2117545,
            'custom_fields': [
                amo_cf(172741, order.email, '380769'),
                amo_cf(172739, order.phone, '380761')
            ]
        }
    ]}
    resp = exec('post', 'contacts', data=data)
    if resp.status_code == 200:
        data = resp.json()
        return jq('._embedded.items[0].id').transform(data)
    else:
        return None


def get_contact_by_email(email):
    query = {'query': email, 'limit_rows': 1}
    resp = exec('get', 'contacts', query=query)
    if resp.status_code == 200:
        data = resp.json()
        return jq('._embedded.items[0].id').transform(data)
    elif resp.status_code == 204:
        return None
    else:
        # handle errors 500, 503
        return None
