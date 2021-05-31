from django.urls import path

from .views      import PosingView

urlpatterns = [
    path('', PosingView.as_view()),
    ]