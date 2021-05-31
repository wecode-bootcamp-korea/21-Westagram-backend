from django.db import models

# Create your models here.

class Account(models.Model):
    email           = models.CharField(max_length=50, unique=True)
    password        = models.CharField(max_length=50)
    nickname        = models.CharField(max_length=50, unique=True, null=True)
    phone_number    = models.CharField(max_length=50, unique=True, null=True)
    class Meta:
        db_table='accounts'
