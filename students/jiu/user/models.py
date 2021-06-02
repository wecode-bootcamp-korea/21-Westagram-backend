from django.db import models

class User(models.Model) :
    nickname     = models.CharField(max_length=30,  unique=True)
    email        = models.EmailField(max_length=50, unique=True, null=False)
    password     = models.CharField(max_length=500,  null=False)
    phone_number = models.CharField(max_length=11,  unique=True, null=False)

    class Meta:
        db_table = 'users'

