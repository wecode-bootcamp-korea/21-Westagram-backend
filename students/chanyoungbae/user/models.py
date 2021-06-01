from django.db import models

# Create your models here.
class User(models.Model):
    
    name      = models.CharField(max_length=45, unique=True)
    email     = models.CharField(max_length=100, unique=True)
    password  = models.CharField(max_length=45)
    phone_num = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = 'users'
