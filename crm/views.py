from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from querystring_parser import parser

from common import mongolog


@csrf_exempt
def web_hook(request):
    data = parser.parse(request.POST.urlencode(), normalized=True)
    mongolog.log('webhook', {'raw_data': request.POST, 'data': data})

    return HttpResponse()
