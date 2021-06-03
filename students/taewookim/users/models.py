from django.db import models

class User(models.Model):
    email        = models.EmailField(max_length=50, unique=True)
    password     = models.CharField(max_length=256)
    nickname     = models.CharField(max_length=40, unique=True)
    phone_number = models.CharField(max_length=13, unique=True)

    class Meta:
        db_table = "users"

class FollowingFollower(models.Model):
    following_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    follower_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')

    class Meta:
        db_table = "following_followers"