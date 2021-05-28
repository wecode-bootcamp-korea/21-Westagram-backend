from django.urls import path

from .views      import UserSignIn 

urlpatterns = [
    path ('/signin',UserSignIn.as_view())
]