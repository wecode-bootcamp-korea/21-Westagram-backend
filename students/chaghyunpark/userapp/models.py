from django.db import models


class User(models.Model):
    nickname         =  models.CharField(max_length=30,unique=True)
    password         =  models.CharField(max_length=1000)
    email            =  models.EmailField(max_length=45,unique=True)
    phone_number     =  models.CharField(max_length=30,unique=True)

    class Meta:
        db_table = 'account'


