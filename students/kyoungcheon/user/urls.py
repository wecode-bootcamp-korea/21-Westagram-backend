from django.urls import path

from .views      import Sign


urlpatterns = [
    path('/Member',Sign.as_view())
]