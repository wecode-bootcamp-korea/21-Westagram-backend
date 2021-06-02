from django.urls import path

from .views import SignupView, LoginView
# from .views import LoginView

urlpatterns = [
    path('sign', SignupView.as_view()),
    path('login', LoginView.as_view())
    
]