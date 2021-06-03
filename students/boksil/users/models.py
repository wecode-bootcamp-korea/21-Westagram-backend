from django.db import models


class User(models.Model):
    password = models.CharField(max_length=90) 
    email    = models.EmailField(max_length=45, unique=True)
    mobile   = models.CharField(max_length=20, null=True) # null=True
    nickname = models.CharField(max_length=45, null=True) # null=True

    class Meta:
        db_table = 'users'