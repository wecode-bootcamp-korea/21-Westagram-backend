from django.urls import path
from user.views  import UserSignUp, UserSignin

urlpatterns = [
    path('/signup', UserSignUp.as_view()),
    path('/signin', UserSignin.as_view())
]