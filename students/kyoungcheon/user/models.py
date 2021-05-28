from django.db import models

# Create your models here.
class Member(models.Model):
    email    = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=200)
    phone    = models.CharField(max_length=50, null=True, unique=True)
    nickname = models.CharField(max_length=45, null=True, unique=True)

    class Meta:
        db_table = 'members'

