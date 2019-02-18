from django.urls import path

from shops.views import processing

app_name = 'shops'

urlpatterns = [
    path('processing/<str:name>', processing, name='processing'),
]
