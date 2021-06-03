from django.db import models

class User(models.Model):
    email    = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=500)
    phone    = models.CharField(max_length=50, unique=True, null=True,)
    nickname = models.CharField(max_length=50, unique=True, null=True,)

    class Meta:
        db_table = 'users'

