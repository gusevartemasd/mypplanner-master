import logging

from django.conf import settings
from telegram.bot import Bot

logger = logging.getLogger(__name__)


def send_message(message):
    """
    TODO: implement notify

    :param message:
    :return:
    """
    logger.info('Send to telegram %s' % (message,))
    try:
        bot = Bot(settings.TELEGRAM_BOT_TOKEN)
        bot.send_message(settings.TELEGRAM_BOT_CHAT_ID, message)
    except Exception as e:
        logger.warn('Failed to send telegram message: %s' % (message,))
