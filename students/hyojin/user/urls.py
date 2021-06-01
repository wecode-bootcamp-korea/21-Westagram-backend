from django.urls import path

from .views import NewUserView

urlpatterns = [
    path('/signup', NewUserView.as_view()),
]
