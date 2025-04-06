from django.urls import path

from .views import landing_view, cached_page_view

urlpatterns = [
    path('', landing_view, name='landing'),
    path('cached/', cached_page_view, name='cached')
]
