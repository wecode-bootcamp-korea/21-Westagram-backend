from django.urls import path
from .views import UserJoinIn

urlpatterns = [
    path('/joinin', UserJoinIn.as_view()),
]