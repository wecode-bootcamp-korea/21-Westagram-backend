import re
import json
from json.encoder import JSONEncoder
from django.db.models.fields import EmailField

from django.db.models.query import QuerySet
from django.views import View
from django.http  import JsonResponse
from django.db.models  import Q

from .models      import User

email_regex = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
password_regex = '^[a-zA-Z0-9!@#$%^&*()-_+={}\|\\\/].{7,}$'

class SignupView(View):

    def post(self, request):
        
        try:
            data = json.loads(request.body)

            nickname     = data.get('nickname')
            email        = data['email']
            password     = data['password']
            phone_number = data.get('phone_number')

            if not email or not password:
                return JsonResponse({'message': 'KEY_ERROR'}, status= 400)
            
            if not re.search(email_regex, email):
                return JsonResponse({'message': '이메일 형식이 아닙니다.'}, status= 400)
            
            if not re.search(password_regex, password):
                return JsonResponse({'message': '패스워드 형식이 아닙니다.'}, status= 400)
              
            if User.objects.filter(
                Q(nickname = nickname) | Q(phone_number = phone_number) | Q(email = email)):
                
                return JsonResponse({'message': '입력값이 중복되었습니다.'}, status= 409)
            
            User.objects.create(
                nickname     = nickname,
                email        = email,
                password     = password,
                phone_number = phone_number
            )
            
            return JsonResponse({'message': 'SUCCESS'}, status= 201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status= 400)

class LoginView(View):
    
    def post(self, request):
        try:
            data = json.loads(request.body)

            account  = data['email']
            password = data['password']

            if not account or not password:
                return JsonResponse({'message': 'KEY_ERROR'}, status= 400)
            
            if not User.objects.filter(email = account):
                return JsonResponse({'message': 'INVALID_USER'}, status= 401)

            if not User.objects.filter(password = password):
                return JsonResponse({'message': 'INVALID_USER'}, status= 401)

            return JsonResponse({'message': 'SUCCESS'}, status= 201)
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status= 400)


