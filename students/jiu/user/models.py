from django.db import models

# Create your models here.
class User(models.Model) :

    nickname    = models.CharField(max_length=30)
    email       = models.EmailField()
    password    = models.CharField(max_length=20)
    phonenumber = models.CharField(max_length=11)

    class Meta:
        db_table = 'users'