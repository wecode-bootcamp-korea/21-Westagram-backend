from django.db import models

class User(models.Model):
    email    = models.EmailField(max_length=128)
    password = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20, null=True)
    contact  = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = 'users'
