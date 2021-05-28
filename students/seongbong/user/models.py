from django.db import models


class User(models.Model):
    email        = models.EmailField(max_length=50)
    password     = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=20)
    nickname     = models.CharField(max_length=20)
    
    class Meta():
        db_table = 'users'