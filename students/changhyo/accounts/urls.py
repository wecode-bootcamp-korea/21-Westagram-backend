from django.urls import path
from .views import NewClient


urlpatterns = [
    path('',NewClient.as_view())

]