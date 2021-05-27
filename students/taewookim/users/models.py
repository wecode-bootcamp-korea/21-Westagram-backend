from django.db import models

class User(models.Model):
    email        = models.EmailField(max_length=50, unique=True, null=False, blank=False)
    password     = models.CharField(max_length=30, null=False, blank=False)
    nickname     = models.CharField(max_length=40, unique=True, null=True, blank=False)
    phone_number = models.CharField(max_length=13, unique=True, null=True, blank=False)

    class Meta:
        db_table = "users"