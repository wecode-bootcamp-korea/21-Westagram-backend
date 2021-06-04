from django.urls import path

from .views      import PostingView

urlpatterns = [
    path('/<int:id>', PostingView.as_view()),
    path('', PostingView.as_view()),
    ]