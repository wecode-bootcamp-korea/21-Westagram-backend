from django.db import models


class User(models.Model):
    mobile   = models.CharField(max_length=20)
    nickname = models.CharField(max_length=45)
    email    = models.EmailField(max_length=45)
    password = models.CharField(max_length=90)

    class Meta():
        db_table = 'users'
