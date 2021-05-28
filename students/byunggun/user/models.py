from django.db import models

class User(models.Model):
    email        = models.CharField(max_length=100, unique=True)
    password     = models.CharField(max_length=45, null=False)
    phone_no     = models.CharField(max_length=45, unique=True)
    full_nm      = models.CharField(max_length=45, null=False)
    user_nm      = models.CharField(max_length=100, unique=True)
    reg_dte      = models.DateTimeField(auto_now_add=True)
    withdraw_dte = models.DateTimeField(null=True)

    class Meta:
        db_table = 'users'