from django.db import models

class User(models.Model):
    email    = models.CharField(max_length=40, unique=True)
    password = models.CharField(max_length=30)
    phone    = models.CharField(max_length=50, blank=True)
    nickname = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = 'users'        
        