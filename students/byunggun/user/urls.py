from django.urls import path
from .views      import UserView, SignIn

urlpatterns = [
    path('', UserView.as_view()),
    path('/signin', SignIn.as_view())
]
