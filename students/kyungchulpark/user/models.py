from django.db   import models

# Create your models here.
class User(models.Model):
    email    = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    nicname  = models.CharField(max_length=50, null=True)
    phone    = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'users'
