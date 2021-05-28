from django.db import models

class User(models.Model):
    email        = models.EmailField(max_length=50)
    password     = models.CharField(max_length=45)
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    nickname     = models.CharField(max_length=45, null=True, blank=True)

    class Meta:
        db_table = 'users'
