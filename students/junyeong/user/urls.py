from django.urls import path

from .views import SignupView
from .views import LoginView
# from .views import LoginView

urlpatterns = [
    path('/sign', SignupView.as_view()),
    path('/login', LoginView.as_view())
    
]