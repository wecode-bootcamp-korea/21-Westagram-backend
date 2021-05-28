from django.db import models
from django    import db

class Signup(models.Model):
    name     = models.CharField(max_length=45, null= True)
    email    = models.CharField(max_length=50)
    password = models.CharField(max_length=45)
    number   = models.CharField(max_length=30, null= True)

    class Meta:
        db_table = 'signups'
