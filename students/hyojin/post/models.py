from django.db import models

from user.models import User

class Post(models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    content      = models.CharField(max_length=200, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'posts'

class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    url  = models.FileField()

    class Meta:
        db_table = 'images' 
