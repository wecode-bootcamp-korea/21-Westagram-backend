from django.urls import path
from user.views  import UserSignUp

urlpatterns = [
    path('', UserSignUp.as_view())
]