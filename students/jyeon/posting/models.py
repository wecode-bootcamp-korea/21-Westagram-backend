from user.models               import User
from django.db                 import models
from django.db.models.deletion import CASCADE
from user.models               import User
from django.utils              import timezone

class Posting(models.Model):
    account = models.ForeignKey('user.User', on_delete=CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    image = models.CharField(max_length=300)
    text = models.TextField(max_length=300)
    
    class Meta:
        db_table = 'postings'

class CharTest(models.Model):
    blank_F_null_F = models.CharField(max_length=20, blank=False, null=False)
    blank_T_null_F = models.CharField(max_length=20, blank=True, null=False)
    blank_F_null_T = models.CharField(max_length=20, blank=False, null=True)
    blank_T_null_T = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'chartests'

class IntTest(models.Model):
    blank_F_null_F = models.IntegerField(blank=False, null=False)
    blank_T_null_F = models.IntegerField(blank=True, null=False)
    blank_F_null_T = models.IntegerField(blank=False, null=True)
    blank_T_null_T = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'inttests'
