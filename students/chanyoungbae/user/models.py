from django.db import models

# Create your models here.
class User(models.Model):
    
    name      = models.CharField(max_length=45, null=True)
    email     = models.CharField(max_length=100)
    password  = models.CharField(max_length=45)
    phone_num = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = 'users'
