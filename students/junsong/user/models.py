from django.db import models

class User(models.Model):
    email = models.EmailField(max_length=128)
    password = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20, blank=True)
    contact = models.IntegerField(null=True)

    class Meta:
        db_table = 'users'
