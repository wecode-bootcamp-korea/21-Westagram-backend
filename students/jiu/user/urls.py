from django.urls import path
from .views      import NewUserView
from .views      import LoginView
 

urlpatterns = [
    path('/signin', NewUserView.as_view()),
    path('/login' , LoginView.as_view())
     ]