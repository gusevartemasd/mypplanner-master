from delivery.models import Delivery
from orders.models import Order, OrderArticle, OrderAddress
from articles.models import Article
from shops.processing.exceptions import (ErrorPackException, InvalidInputDataException, InvalidDeliveryException,
                                         BadDaDataBalanceException, InvalidAddressException, InvalidArticlesException)
from shops.utils import get_full_name_part, FIRST_NAME_PART, LAST_NAME_PART, MIDDLE_NAME_PART
from stock.pack import pack
from shops import normalize


def processing_tilda(data: dict):
    """
    Создание заказа от Тильды
    :param data: dict
    :return: Order|None
    """
    if not is_valid_data(data):
        raise InvalidInputDataException(data)

    order = create_order(data)
    create_articles(order, data['payment']['products'])

    try:
        pack(order)
    except Exception as e:
        raise ErrorPackException(order, e)

    if not order.delivery:
        raise InvalidDeliveryException(order)
    elif order.address.result is None and order.address.unparsed_parts is None:
        raise BadDaDataBalanceException(order)
    elif order.address.unparsed_parts is not None:
        raise InvalidAddressException(order)
    else:
        return order


def is_valid_data(data):
    required_keys = {'Dostavka', 'Address', 'payment', 'Email', 'Phone', 'Name', 'paymentsystem', 'formid', 'formname'}
    keys = set(data.keys())
    if not required_keys.issubset(keys):
        return False

    required_keys = {'orderid', 'amount', 'products'}
    keys = set(data['payment'].keys())
    if not required_keys.issubset(keys):
        return False

    return True


def create_order(data):
    order = Order()

    order.address = data['Address']
    order.delivery = load_delivery(data['Dostavka'])
    #normalized_name = normalize.name(data['Name'])
    #order.full_name = normalized_name if normalized_name else data["Name"]
    #order.first_name = get_full_name_part(normalized_name, FIRST_NAME_PART)
    #order.middle_name = get_full_name_part(normalized_name, MIDDLE_NAME_PART)
    #order.last_name = get_full_name_part(normalized_name, LAST_NAME_PART)
    order.first_name = data['name']
    order.middle_name = data['name']
    order.last_name = data['name']

    order.phone = data['Phone']
    order.email = data['Email']
    order.comment = data.get('Comment', '')
    order.is_payed = is_payed(data['paymentsystem'])
    order.payment_system = data['paymentsystem']
    order.total = data['payment']['amount']
    order.payment_id = data['payment']['orderid']
    order.promo_code = data.get('Промокод', '')

    order.save()
    order.refresh_from_db()
    return order


def load_address(address_source):
    address = OrderAddress()
    address.source = address_source
    address.postal_code = ''

    res = normalize.address(address_source)
    if res is not None:
        address.result = res.result
        address.postal_code = res.postal_code
        address.country = res.country
        address.region = res.region
        address.region_fias_id = res.region_fias_id
        address.region_type = res.region_type
        address.area = res.area
        address.area_fias_id = res.area_fias_id
        address.area_type = res.area_type
        address.city = res.city
        address.city_fias_id = res.city_fias_id
        address.city_type = res.city_type
        address.city_district = res.city_district
        address.city_district_fias_id = res.city_district_fias_id
        address.city_district_type = res.city_district_type
        address.settlement = res.settlement
        address.settlement_fias_id = res.settlement_fias_id
        address.settlement_type = res.settlement_type
        address.street = res.street
        address.street_fias_id = res.street_fias_id
        address.street_type = res.street_type
        address.house = res.house
        address.house_fias_id = res.house_fias_id
        address.house_type = res.house_type
        address.block = res.block
        address.block_type = res.block_type
        address.flat = res.flat
        address.flat_type = res.flat_type
        address.geo_lat = res.geo_lat
        address.geo_lon = res.geo_lon
        address.unparsed_parts = res.unparsed_parts

    address.save()

    return address


def load_delivery(parse_rule):
    try:
        return Delivery.objects.get(parse_rule=parse_rule)
    except Delivery.DoesNotExist:
        return None


def create_articles(order, items):
    invalid_items = list()

    for item in items:
        try:
            article = Article.objects.get(sku=item['sku'])
            OrderArticle.objects.create(order=order, article=article, quantity=item['quantity'])
        except Article.DoesNotExist:
            invalid_items.append(item)

    if len(invalid_items) > 0:
        raise InvalidArticlesException(order, invalid_items)


def is_payed(payment_system):
    return payment_system != 'banktransfer'
