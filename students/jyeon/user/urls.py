from django.urls import path

from .views      import UserSignupView
from .views      import UserSigninView

urlpatterns = [
    path('/signup', UserSignupView.as_view()),
    path('/signin', UserSigninView.as_view()),
]