from django.urls import path

from .views import JoinView

urlpatterns = [
   path('/join', JoinView.as_view())  
]
