from django.db import models

from .validations import validate_email, validate_password

class User(models.Model):
    email        = models.CharField(max_length=70, unique=True, validators=[validate_email])
    password     = models.CharField(max_length=45, validators=[validate_password])
    phone_number = models.CharField(max_length=30, unique=True, blank=True, null=True)
    nickname     = models.CharField(max_length=45, unique=True, blank=True, null=True)

    def check_blank(self, value):
        if value == "":
            return None
        else: 
            return value
 
    class Meta:
        db_table='users'

