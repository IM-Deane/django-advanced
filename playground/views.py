import requests

from django.shortcuts import render
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework.views import APIView



def say_hello(request):
    """
    This view cache's the response from a slow 3rd party API
    and then display's the result.

    The first time you load the view, the data takes about 2
    seconds to resolve and cache the result.

    Subsequent requests will be resolve much quicker as Django
    grabs the data from the cache instead of the API.
    """
    key = 'httpbin_result'
    if cache.get(key) is None:
        response = requests.get('https://httpbin.org/delay/2')
        data = response.json()
        cache.set(key, data)

    return render(request, 'hello.html', {'name': cache.get(key)})


@cache_page(5 * 60)
def cached_view(request):
    """
    We can also cache an entire view instead of individual responses
    like the endpoint above.
    """
    response = requests.get('https://httpbin.org/delay/2')
    data = response.json()
    return render(request, 'hello.html', {'name': data})


class CachedClassView(APIView):
    """
    We can also cache class based views like this.

    Kinda janky looking I know, but it works.
    """
    @method_decorator(cache_page(5 * 60))
    def get(self, request):
        response = requests.get('https://httpbin.org/delay/2')
        data = response.json()
        return render(request, 'hello.html', {'name': data})