from django.db import models

class User(models.Model):
    email     = models.EmailField(max_length=128, unique=True)
    password  = models.CharField(max_length=45)
    phone_num = models.CharField(max_length=45, unique=True)
    nick_name = models.CharField(max_length=45, unique=True)

    class Meta:
        db_table = 'users'