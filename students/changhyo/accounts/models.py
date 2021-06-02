from django.db import models

# Create your models here.
class SignUp(models.Model):
    email     = models.EmailField(max_length = 300)
    password  = models.CharField(max_length =190)
    phone_num = models.CharField(max_length = 15)
    nickname  = models.CharField(max_length = 100)

    class Meta:
        db_table = "signup"

