import json

from orders.models import Order


class ProcessingException(Exception):
    message = ""

    def __str__(self):
        return self.message


class InvalidInputDataException(ProcessingException):
    def __init__(self, data):
        self.message = 'Неверные входные данные: ' + '\n' + json.dumps(data)


class BadDaDataBalanceException(ProcessingException):
    def __init__(self, order: Order) -> None:
        self.message = 'Баланс DaData исчерпан'
        self.order = order


class InvalidDeliveryException(ProcessingException):
    def __init__(self, order: Order) -> None:
        self.message = 'Неверный способ доставки'
        self.order = order


class ForeignDeliveryException(ProcessingException):
    def __init__(self, order: Order) -> None:
        self.message = 'Доставка в другую страну'
        self.order = order


class InvalidAddressException(ProcessingException):
    def __init__(self, order: Order) -> None:
        self.message = 'Некорректный адрес достваки'
        self.order = order


class InvalidArticlesException(ProcessingException):
    def __init__(self, order: Order, invalid_items: list) -> None:
        self.order = order
        self.message = 'Не найдены артикли ' + json.dumps(invalid_items)


class ErrorPackException(ProcessingException):
    def __init__(self, order: Order, e) -> None:
        self.order = order
        self.message = 'Ошибка расчета коробок: %s' % e


class AddressNormalizationException(ProcessingException):
    def __init__(self, order: Order) -> None:
        self.order = order
        self.message = 'Ошибка нормализации адреса (Почта России)'


class SdekNotImplementedException(ProcessingException):
    def __init__(self, order: Order) -> None:
        self.order = order
        self.message = 'функционал отправки СДЭК не реализован'
