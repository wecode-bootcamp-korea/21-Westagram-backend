from enum import unique
from django.core.validators import validate_integer
from django.db              import models


class User(models.Model):
    email        = models.EmailField(max_length = 80, null = False, unique = True)
    password     = models.CharField(max_length = 100, null = False)
    nickname     = models.CharField(max_length = 30, unique = True)
    phone_number = models.CharField(max_length = 13, unique = True) # 010 -0000-0000 try applying 

    class Meta:
        db_table = 'users'