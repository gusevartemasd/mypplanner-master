import requests
from crm.api import exec


def load_articles(request):
    resp = exec('get', 'catalog_elements', {'catalog_id': 4001})
    resp.json()


