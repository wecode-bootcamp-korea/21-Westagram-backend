from django.urls import path
from .views import SignUpView, SignInView

urlpatterns = [
    path('/Signup', SignUpView.as_view()),
    path('/Signin', SignInView.as_view())
]
