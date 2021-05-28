from enum import unique
from django.core.validators import validate_integer
from django.db import models


class User(models.Model):
    email = models.EmailField(max_length= 80, null=False)
    password = models.CharField(max_length = 30,null=False)
    nickname = models.CharField(max_length = 30)
    phone_number = models.CharField(max_length = 13) # 010 -0000-0000 try applying django.core.validators

    class Meta:
        db_table = 'users'