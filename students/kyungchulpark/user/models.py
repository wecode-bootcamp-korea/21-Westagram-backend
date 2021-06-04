from django.db   import models

# Create your models here.
class User(models.Model):
    email        = models.EmailField(max_length=50)
    password     = models.CharField(max_length=200)
    nickname     = models.CharField(max_length=50, null=True)
    phone_number = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'users'
