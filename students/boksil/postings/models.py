from django.db import models
from django.db.models.deletion import CASCADE

from users.models import User # PK

class Posting(models.Model):
    atime   = models.DateTimeField(auto_now_add=True)
    image   = models.ImageField()
    content = models.CharField(max_length=200)
    user    = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'postings'