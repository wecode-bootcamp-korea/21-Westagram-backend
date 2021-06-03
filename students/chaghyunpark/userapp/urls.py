from django.urls import path
from.views       import SignView
from.views       import LoginView
urlpatterns = [
    path('/sign',SignView.as_view()),
    path('/login',LoginView.as_view()),

]
