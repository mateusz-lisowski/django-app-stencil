from django.shortcuts import render
from django.views.decorators.cache import cache_page

@cache_page(60)
def landing_view(request):
    return render(request, 'landing/landing.html')
