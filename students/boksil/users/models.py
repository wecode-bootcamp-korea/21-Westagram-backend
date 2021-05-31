from django.db import models


class User(models.Model):
    email    = models.EmailField(max_length=45) # unique=True 중복없게 만들어줌
    # null=True 라고 지정했는데 ("Column 'mobile' cannot be null")
    mobile   = models.CharField(max_length=20, null=True) # null=True
    nickname = models.CharField(max_length=45, null=True) # null=True
    password = models.CharField(max_length=90) 

    class Meta():
        db_table = 'users'
