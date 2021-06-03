from django.urls import path

from .views import NewUserView, SignInView

urlpatterns = [
    path('/signup', NewUserView.as_view()),
    path('/signin', SignInView.as_view())
]
