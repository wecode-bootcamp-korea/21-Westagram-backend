from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import IntegerField

class User(models.Model):
    email     = models.EmailField(max_length=128, unique=True)
    password  = models.CharField(max_length=45)
    phone_num = models.CharField(max_length=45, unique=True, blank=True, null=True)
    nick_name  = models.CharField(max_length=45, unique=True, blank=True, null=True)
    
    class Meta:
        db_table = 'user'

