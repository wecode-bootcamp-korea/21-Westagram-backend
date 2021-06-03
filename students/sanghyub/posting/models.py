from enum       import unique
from django.db  import models
from django.db.models.deletion import CASCADE
from user.models import User

class Posting(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    context = models.TextField()
 
    class Meta:
        db_table = 'postings'

class Image(models.Model):
    image = models.CharField(max_length = 300)
    posting = models.ForeignKey(Posting, on_delete = CASCADE)

    class Meta:
        db_table = 'images'

