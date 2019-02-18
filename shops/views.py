import logging

from django.db import transaction, IntegrityError
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from querystring_parser import parser

from common import mongolog
from crm.api import create_order as amo_create_order
from delivery import providers
from notifications.sms import send_sms
from shops.processing.tilda import processing_tilda
from shops.processing.exceptions import *
from notifications.telegram import send_message

logger = logging.getLogger(__name__)


@csrf_exempt
@transaction.atomic
def processing(request, name):
    logger.info(request.body.decode('utf-8'))
    data = parser.parse(request.POST.urlencode(), normalized=True)

    mongolog.log('processing', {'name': name, 'data': data})

    try:
        if name == 'tilda':
            order = processing_tilda(data)
        else:
            return HttpResponse(status=404)

        if not order.is_payed:
            send_sms(order.phone, 'unpaid', {'total': order.total + order.delivery.cost})
            # TODO: send email

        order.amo_order_id = str(amo_create_order(order))
        order.save()

    except InvalidInputDataException as e:
        send_message(str(e))
    except BadDaDataBalanceException as e:
        send_message('Недостаточный баланс на https://dadata.ru')
        amo_create_order(e.order, str(e))
    except InvalidDeliveryException as e:
        amo_create_order(e.order, str(e))
    except ForeignDeliveryException as e:
        amo_create_order(e.order, str(e))
    except InvalidAddressException as e:
        amo_create_order(e.order, str(e))
    except InvalidArticlesException as e:
        amo_create_order(e.order, str(e))
    except ErrorPackException as e:
        amo_create_order(e.order, str(e))
    except AddressNormalizationException as e:
        amo_create_order(e.order, str(e))
    except SdekNotImplementedException as e:
        amo_create_order(e.order, str(e))
    except IntegrityError as e:
        return HttpResponse('ok', status=200)

    return HttpResponse('ok', status=200)

