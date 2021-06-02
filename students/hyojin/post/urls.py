from django.urls import path

from .views import AllPostView, PostUploadView

urlpatterns = [
    path('/upload', PostUploadView.as_view()),
    path('/getalllist', AllPostView.as_view())
]
