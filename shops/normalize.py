from dadata.plugins import DjangoDaDataClient


def address(source):
    client = DjangoDaDataClient()
    client.address = source
    if client.address.request() == 200:
        return client.result
    return None


def name(source):
    client = DjangoDaDataClient()
    client.fio = source
    if client.fio.request() == 200:
        return client.result.result
    return source


def phone(source):
    client = DjangoDaDataClient()
    client.phone = source
    if client.phone.request() == 200:
        return client.result.phone
    return source
