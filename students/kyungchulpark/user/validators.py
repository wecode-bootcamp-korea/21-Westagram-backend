import re

from django.core.exceptions import ValidationError
from .models                import User
from xxlimited              import Null

def validate_email(email):
    if email==Null or email=='':
        raise ValidationError('EMAIL CHECK')
    elif (bool(re.search('@',email))==False) or (bool(re.search('.',email))==False):
        raise ValidationError('MUST WRITE @, . ')
    elif User.objects.filter(email=email).exists():
        raise ValidationError('EMAIL EXIST')

def validate_password(password):
    if password==Null or password=='':
        raise ValidationError('PASSWORD CHECK')
    elif len(password)<8 and len(password)>0:
        raise ValidationError('PASSWORD MIN LENGTH 8')

def validate_phone(phone):
    if bool(re.search('^(\d{2,3}).*(\d{3,4}).*(\d{4})$',phone))==False and len(phone)>0:
        raise ValidationError('PHONE NUMBER CHECK')
    elif User.objects.filter(phone=phone).exists() and phone!=Null and phone!='':
        raise ValidationError('PHONE NUMBER EXIST')

def validate_nicname(nicname):
    if User.objects.filter(nicname=nicname).exists() and nicname!=Null and nicname!='':
        raise ValidationError('NICNAME EXIST')