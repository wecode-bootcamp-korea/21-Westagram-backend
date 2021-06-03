from django.urls import path

from .views import Post_updateView, PostingView

# from .views import LoginView

urlpatterns = [
    path('post', PostingView.as_view()),   
    path('update',Post_updateView.as_view())
]