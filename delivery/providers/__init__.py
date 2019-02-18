from common import mongolog
from delivery.models import Delivery
from delivery.providers import russian_post, sdek
from orders.models import Order
from shops.processing.exceptions import SdekNotImplementedException


def post(order: Order):
    if order.delivery.provider == Delivery.Providers.RUSSIAN_POST.value:
        response = russian_post.post(order)

        mongolog.log('delivery', {
            'name': "russian_post",
            'order_id': order.id,
            'data': response,
        })

        ship_id = response['result-ids'][0]

        return russian_post.request_barcode(ship_id)
    elif order.delivery.provider == Delivery.Providers.SDEK.value:
        response = sdek.post(order)

        return ''
    else:
        raise ValueError
