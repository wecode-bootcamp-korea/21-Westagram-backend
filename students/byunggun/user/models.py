from django.db import models

class User(models.Model):
    email        = models.CharField(max_length=100, unique=True)
    password     = models.CharField(max_length=45, null=False)
    phone_number = models.CharField(max_length=45, unique=True)
    full_name    = models.CharField(max_length=45, null=False)
    user_name    = models.CharField(max_length=100, unique=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    deleted_at   = models.DateTimeField(null=True)

    class Meta:
        db_table = 'users'