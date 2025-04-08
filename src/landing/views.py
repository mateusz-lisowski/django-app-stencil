import datetime

from django.views.decorators.cache import cache_page
from django.shortcuts import render


def landing_view(request):
    return render(request, 'landing/landing.html')


@cache_page(60 * 1)
def cached_page_view(request):
    now = datetime.datetime.now()
    formatted_time = now.strftime("%H:%M:%S")
    return render(request, 'landing/cached.html', {'time': formatted_time})
