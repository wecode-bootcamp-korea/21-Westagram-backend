from django.db      import models
from userapp.models import User 

class Postboard(models.Model):
    user         = models.ForeignKey(User,on_delete=models.CASCADE)
    contensboard = models.TextField(max_length=4000,null=True)
    img_url      = models.URLField(max_length=400)
    time         = models.DateTimeField(auto_now_add=True)

class Meta:
    db_table ="Pyboard" #개인+게시물