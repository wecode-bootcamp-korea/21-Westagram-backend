from django.db import models

class User(models.Model):
    account         = models.CharField(max_length=50, unique=True)
    password        = models.CharField(max_length=200)
    phone_number    = models.CharField(max_length=50, unique=True)
    nickname        = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'users'