from django.urls import path
from .views import UserJoinIn, UserLogIn

urlpatterns = [
    path('/joinin', UserJoinIn.as_view()),
    path('/login', UserLogIn.as_view())
]