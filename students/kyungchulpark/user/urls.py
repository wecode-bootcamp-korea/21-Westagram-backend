from django.urls import path
from .views      import UserView

urlpatterns = [
    path('/account',UserView.as_view())
]
