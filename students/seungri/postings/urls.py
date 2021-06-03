from django.urls import path

urlpatterns = [
    path('', UserJoinIn.as_view()),
]