from django.urls import path
from .views import NewClient,Login


urlpatterns = [
    path('/signup',NewClient.as_view()),
    path('/signin',Login.as_view())

]