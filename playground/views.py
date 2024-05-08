from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
import logging
import requests

logger = logging.getLogger(__name__)

class HelloView(APIView):
    def get(self, request):
        try:
            logger.info('calling httpbin')
            response = requests.get('https://httpbin.org/delay/2')
            data = response.json()
        except request.ConnectionError:
            logger.critical('httpbin ')
        return render(request, 'hello.html', {'name': data})





    