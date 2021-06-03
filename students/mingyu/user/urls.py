from django.urls import path

from user.views import SigninView, SignupView

urlpatterns = [
   path('/signup', SignupView.as_view()),
   path('/signin', SigninView.as_view())
]
