from django.db import models


class User(models.Model):
    email    = models.EmailField(max_length=45, unique=True)
    mobile   = models.CharField(max_length=20, null=True, blank=False) # null=True
    nickname = models.CharField(max_length=45, null=True, blank=False) # null=True
    password = models.CharField(max_length=90) 

    class Meta:
        db_table = 'users'