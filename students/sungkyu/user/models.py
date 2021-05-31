from django.db import models

class User(models.Model):
    email        = models.EmailField(unique=True, max_length=50)
    password     = models.CharField(max_length=45)
    phone_number = models.CharField(max_length=45)
    nickname     = models.CharField(max_length=45)

    class Meta:
        db_table = 'users'