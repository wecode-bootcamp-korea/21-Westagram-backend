from django.urls import path
from .views import SignupListView

urlpatterns = [
    path('', SignupListView.as_view())
]