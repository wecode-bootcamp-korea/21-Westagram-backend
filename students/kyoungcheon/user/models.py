from django.db import models

# Create your models here.
class Member(models.Model):
    email    = models.EmailField(max_length=100)
    password = models.CharField(max_length=200)
    phone    = models.IntegerField()
    nickname = models.CharField(max_length=45)

    class Meta:
        db_table = 'members'

