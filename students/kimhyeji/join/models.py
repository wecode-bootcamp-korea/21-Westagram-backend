from django.db import models



# Create your models here.

class Join(models.Model):
    email = models.EmailField(max_length=100, unique=True)
    user_name =models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    phon_number = models.CharField(max_length=100 , null =True , unique=True)
    nick_name = models.CharField(max_length=100, unique=True , null =True)
    

    class Meta():
        db_table = 'joins'

