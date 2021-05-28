from django.db import models

class User(models.Model):
    email        = models.EmailField(max_length=45, unique=True)
    password     = models.CharField(max_length=45)
    nickname     = models.CharField(max_length=45, unique=True)
    phone_number = models.IntegerField(unique=True)

    class Meta:
        db_table = 'users'

