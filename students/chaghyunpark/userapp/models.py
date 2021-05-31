from django.db import models


class User(models.Model):
    nickname         =  models.CharField(max_length=30)
    password         =  models.CharField(max_length=30)
    email            =  models.EmailField(max_length=45,unique=True)
    phone_number     =  models.CharField(max_length=30)

    class Meta:
        db_table = 'account'

