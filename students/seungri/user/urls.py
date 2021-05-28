from django.urls import path
from .views import UserJoinIn

urlpatterns = [
    path('/users', UserJoinIn.as_view())
]