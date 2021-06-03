import json
import re
import bcrypt
import jwt

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q

from mysettings       import SECRET_KEY
from .models          import User

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            email             = data['email']
            phone             = data.get('phone')
            nickname          = data.get('nickname')   
            hased_password    = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            email_REGEX       = '^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$'
           
            q = Q()

            if '' == email:
                return JsonResponse({'message':'USER_ID_IS_EMPTY'}, status=400)
            if '' == data['password']:
                return JsonResponse({'message':'PASSWORD_IS_EMPTY'}, status=400)
            if not re.match (email_REGEX, email):
                return JsonResponse({'message':'INVALID_EMAIL_FORMAT'}, status=400)
            if len(data['password']) < 8:
                return JsonResponse({'message':'TOO_SHORT_PASSWORD'}, status=400) 
            if User.objects.filter(Q(email = email) | Q(phone = phone) | Q(nickname = nickname)).exists():
                return JsonResponse({'message':'ALREADY_EXISTS'}, status=400)
        
            User.objects.create(
                email    = email,
                password = hased_password, 
                phone    = phone,
                nickname = nickname
            )
            return JsonResponse({'message':'SUCCESS'}, status=201)
        except KeyError: 
            return JsonResponse({'message':'KEY_ERROR'}, status=400) 
        except User.DoesNotExist:
            return JsonResponse ({'message':'USER_DOSE_NOT_EXIST'}, status=400)

class SignInView(View):
    def post(self, request):
        try:
            data        = json.loads(request.body)
            email       = data['email']
            password    = data['password']
            user        = User.objects.get(email=data['email'])
            email_Regex = '^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$'
            
            if not re.match (email_Regex, email):
                return JsonResponse({'message':'INVALID_EMAIL_FORMAT'}, status=400)
            if not User.objects.filter(Q(email = data['email'])).exists():
                return JsonResponse({'message':'INVALID_USER'}, status=401)
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                access_token = jwt.encode({'id':user.id}, SECRET_KEY, algorithm ='HS256')
                #access_token =  access_token.decode('utf-8')
                return JsonResponse({'token':access_token, 'message':'SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse ({'message':'KEY_ERROR'}, status=400) 
        except ValueError:
            return JsonResponse({'message' :'VALUE_ERROR'}, status=400)   
        except User.DoesNotExist:
            return JsonResponse ({'message':'USER_DOSE_NOT_EXIST'}, status=400)
