from django.urls import path

from .views import UserSignupView

urlpatterns = [
    path('/usersignup', UserSignupView.as_view())
]