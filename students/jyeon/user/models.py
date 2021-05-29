from django.db import models

# Create your models here.

class User(models.Model):
    account         = models.CharField(max_length=50, unique=True)
    password        = models.CharField(max_length=50, unique=True)
    phone_number    = models.CharField(max_length=50, unique=True)
    nickname        = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'users'
