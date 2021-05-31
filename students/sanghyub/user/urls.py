from django.urls import path

from .views      import UserSignUp 

urlpatterns = [
    path ('/signup',UserSignUp.as_view())
]