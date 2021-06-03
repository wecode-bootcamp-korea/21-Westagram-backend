from django.db import models

class User(models.Model):
    email        = models.EmailField(max_length=100, unique=True)
    password     = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100, null=True, unique=True)
    nick_name    = models.CharField(max_length=100, null=True, unique=True)
    
    class Meta:
        db_table = 'users'

