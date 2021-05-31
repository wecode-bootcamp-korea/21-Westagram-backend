from django.urls import path

from .views      import SignUp


urlpatterns = [
    path('/member',SignUp.as_view())
]