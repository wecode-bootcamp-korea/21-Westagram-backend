from django.urls import path
from .views      import NewUserView
 

urlpatterns = [
    path('/signin', NewUserView.as_view())
     ]
