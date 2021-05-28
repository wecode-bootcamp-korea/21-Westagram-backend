from django.db import models

class Users(models.Model):
    email       = models.EmailField(max_length=50)
    password    = models.CharField(max_length=45)
    phonenumber = models.CharField(max_length=45)
    nickname    = models.CharField(max_length=45)


    class Meta:
        db_table = 'users'