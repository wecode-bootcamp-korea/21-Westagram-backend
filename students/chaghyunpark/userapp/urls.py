from django.urls import path
from.views       import UserView
from.views       import LogView
urlpatterns = [
    path('/user',UserView.as_view()),
    path('/log',LogView.as_view()),

]
