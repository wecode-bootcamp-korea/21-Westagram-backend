from django.db    import models



class User(models.Model):
    nickname         =  models.CharField(max_length=6 )
    password         =  models.CharField(max_length=30)
    email            =  models.EmailField(max_length=45)
    phone_number     =  models.CharField()



    class Meta:
        db_table = 'account'
