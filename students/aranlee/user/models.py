from django.db import models


class User(models.Model):
    user_email = models.CharField(max_length=40, default=None, unique=True)
    password   = models.CharField(max_length=30, default=None)
    phone      = models.CharField(max_length=50, blank=True)
    nickname   = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = 'users' 

        


        