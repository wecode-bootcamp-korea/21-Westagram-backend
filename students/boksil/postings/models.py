from django.db import models

from users import models # PK

class Posting(models.Model):
    atime   = models.DateTimeField(auto_now_add=True)
    image   = models.ImageField()
    content = models.CharField(max_length=200)
    user    = models.ForeignKey(models.User)

    class Meta:
        db_table = 'postings'