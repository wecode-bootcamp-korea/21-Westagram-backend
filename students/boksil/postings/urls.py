from django.urls import path
from .views      import PostUploadView

urlpatterns = [
    path('/upload', PostUploadView.as_view())
]