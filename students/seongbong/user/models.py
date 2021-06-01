from django.db import models


class User(models.Model):
    email        = models.EmailField(max_length=50, unique=True)
    password     = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=20, blank=True)
    nickname     = models.CharField(max_length=20, blank=True)
    
    class Meta:
        db_table = 'users'