from django.db import models
from django.utils import timezone

class Post(models.Model):
    user        = models.ForeignKey()
    create_time = 
    image_url   =

    class Meta:
        db_table = 'postings'