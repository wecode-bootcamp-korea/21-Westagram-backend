from django.db import models


# Create your models here.
class User(models.Model) :

    nickname    = models.CharField(max_length=30)
    email       = models.EmailField(max_length=50, unique=True, null=False)
    password    = models.CharField(max_length=20,  unique=True, null=False)
    phonenumber = models.CharField(max_length=11,  unique=True)

    class Meta:
        db_table = 'users'