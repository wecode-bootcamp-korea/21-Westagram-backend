import re

from django.core.exceptions import ValidationError
from .models                import User


def validate_email(email):
    if email==None or email=='':
        raise ValidationError('EMAIL CHECK')
    if (bool(re.search('^([a-z0-9_+.-]+@([a-z0-9-]+\.)+[a-z0-9]{2,4}){1,50}$',email))==False):
        raise ValidationError('MUST WRITE @, . ')
    if User.objects.filter(email=email).exists():
        raise ValidationError('EMAIL EXIST')

def validate_password(password):
    if password==None or password=='':
        raise ValidationError('PASSWORD CHECK')
    if len(password)<8 and len(password)>0:
        raise ValidationError('PASSWORD MIN LENGTH 8')

def validate_phone(phone_number):
    if bool(re.search('^(\d{2,3}).*(\d{3,4}).*(\d{4})$',phone_number))==False and len(phone_number)>0:
        raise ValidationError('PHONE NUMBER CHECK')
    if User.objects.filter(phone_number=phone_number).exists() and phone_number!=None and phone_number!='':
        raise ValidationError('PHONE NUMBER EXIST')

def validate_nickname(nickname):
    if User.objects.filter(nickname=nickname).exists() and nickname!=None and nickname!='':
        raise ValidationError('NICKNAME EXIST')


    
    