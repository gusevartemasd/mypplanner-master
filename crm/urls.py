from django.urls import path
from crm.views import web_hook

app_name = 'crm'

urlpatterns = [
    path('webhook', web_hook, name='webhook'),
]
