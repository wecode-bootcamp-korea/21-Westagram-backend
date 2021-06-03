from django.db import models
from user.models import User

class Board(models.Model):
    title       = models.CharField(max_length=30)
    contents    = models.CharField(max_length=500)
    create_time = models.DateTimeField(auto_now_add=True)
    user      = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'boards'

class Image(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    picture = models.CharField(max_length=200)

    class Meta:
        db_table = 'images'
