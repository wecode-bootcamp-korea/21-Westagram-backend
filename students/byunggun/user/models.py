from django.db               import models
from django.db.models.fields import CharField, DateTimeField

class User(models.Model):
    email        = CharField(max_length=100, unique=True)
    password     = CharField(max_length=45, null=False)
    phone_no     = CharField(max_length=45, unique=True)
    full_nm      = CharField(max_length=45, null=False)
    user_nm      = CharField(max_length=100, unique=True)
    reg_dte      = DateTimeField(auto_now_add=True)
    withdraw_dte = DateTimeField(null=True)

    class Meta:
        db_table = 'users'