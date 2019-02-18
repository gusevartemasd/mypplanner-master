from urllib.parse import urlencode

import requests
from django.conf import settings
from django.template.loader import get_template


def send_sms(phone, template, context):
    tpl_ns = '/'.join(['sms', template])
    text = get_template('/'.join([tpl_ns, 'template.txt']))

    sms_content = text.render(context)

    params = {
        'login': settings.SMSC_LOGIN,
        'psw': settings.SMSC_PASSWORD,
        'charset': 'utf-8',
        'phones': phone,
        'mes': sms_content,
    }

    url = 'https://smsc.ru/sys/send.php?' + urlencode(params)
    requests.get(url)
