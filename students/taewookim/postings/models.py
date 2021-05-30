from django.db                       import models
from django.db.models.fields.related import ForeignKey

class Posting(models.Model):
    user       = ForeignKey('users.user', on_delete=models.CASCADE)
    title      = models.fields.CharField()
    main_text  = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class PostingImage(Posting):
    posting = ForeignKey(Posting, on_delete=models.CASCADE)
    url     = models.CharField(max_length=200)
    
    class Meta():
        db_table = 'posting_images'