from django.db import models


class User(models.Model):
    user_name    = models.CharField(max_length=45)
    phone_number = models.CharField(max_length=45)
    user_email   = models.CharField(max_length=45)
    passward     = models.CharField(max_length=45)
    
    class Meta:
        db_table = "users"