
from django.urls import path

from .views      import UserPost

urlpatterns = [
    path ('/create',UserPost.as_view()),
]