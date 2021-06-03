from django.db import models

class User(models.Model):
    user_name    = models.CharField(max_length=45, unique=True)
    phone_number = models.CharField(max_length=45, unique=True)
    user_email   = models.CharField(max_length=50, unique=True, null=False)
    password     = models.CharField(max_length=200, null=False)

    class Meta:
        db_table = "users"