import logging
import requests

from django.shortcuts import render

logger = logging.getLogger(__name__)


def say_hello(request):
    """
    Add logging error handling
    """
    try:
        logger.info('Calling httpbin')
        response = requests.get('https://httpbin.org/delay/2')
        logger.info('Recieved the response')
    except requests.ConnectionError:
        logger.critical('httpbin is offline!')
    return render(request, 'hello.html', {'name': 'Logger'})
