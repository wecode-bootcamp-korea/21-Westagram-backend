from django.urls import path

from .views      import UserView, LoginView, follow_user, unfollow_user, get_follower, get_following

urlpatterns = [
    path('', UserView.as_view()),
    path('/<int:following_user_id>/follow', follow_user),
    path('/<int:following_user_id>/unfollow', unfollow_user),
    path('/<int:user_id>/follower', get_follower),
    path('/<int:user_id>/following', get_following),
    path('/login', LoginView.as_view()),
]