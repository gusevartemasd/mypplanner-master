import logging

from django.conf import settings
from pymongo import MongoClient

logger = logging.getLogger(__name__)


def log(namespace, data):
    try:
        client = MongoClient(settings.MONGODB_URL)
        db = client.get_default_database()
        db.get_collection(namespace).insert_one(data)
    except Exception as e:
        logger.warn('Error save log in mongodb: %s' % (e,))
