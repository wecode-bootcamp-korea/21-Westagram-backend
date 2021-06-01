from django.urls import path

from .views import PostingView

urlpatterns = [
    path('/upload', PostingView.as_view()),
    path('/list', PostingView.as_view())
]