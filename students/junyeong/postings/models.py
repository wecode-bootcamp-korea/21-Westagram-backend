from django.db import models

from user.models import User
# Create your models here.

class Posting(models.Model):
    time    = models.TimeField(auto_now_add=True)
    img_url = models.URLField()
    user    = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'postings'