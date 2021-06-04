from django.db                 import models
from django.db.models.deletion import CASCADE

from user.models               import User

class Posting(models.Model):
    account       = models.ForeignKey('user.User', on_delete=CASCADE)
    datetime      = models.DateTimeField(auto_now_add=True)
    posting_text  = models.TextField(max_length=300)
    
    class Meta:
        db_table = 'postings'

class Image(models.Model):
    posting_text  = models.ForeignKey('Posting', on_delete=CASCADE)
    posting_image = models.CharField(max_length=300)

    class Meta:
        db_table = 'images'