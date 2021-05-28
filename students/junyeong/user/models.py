from django.db import models
from django    import db

class Signup(models.Model):
    nickname     = models.CharField(max_length =45, null= True, unique=True)
    email        = models.EmailField(max_length=50, unique=True)
    password     = models.CharField(max_length =45)
    phone_number = models.CharField(max_length =30, null= True, unique=True)

    class Meta:
        db_table = 'signups'
