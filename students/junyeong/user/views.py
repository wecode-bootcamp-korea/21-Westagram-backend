import json
import re
from json.encoder import JSONEncoder

from django.views import View
from django.http  import JsonResponse

from .models      import Signup

email_regex = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
password_regex = '^[a-zA-Z0-9!@#$%^&*()-_+={}\|\\\/].{7,}$'

class SignupListView(View):

    def post(self, request):
        data = json.loads(request.body)
        
        try:
    
            nickname     = data['nickname']
            email        = data['email']
            password     = data['password']
            phone_number = data['phone_number']

            if not email or not password:
                return JsonResponse({'message': 'KEY_ERROR'}, status= 400)
            
            if re.search(email_regex, email) == None:
                return JsonResponse({'message': '이메일 형식이 아닙니다.'}, status= 400)
            
            if re.search(password_regex, password) == None:
                return JsonResponse({'message': '패스워드 형식이 아닙니다.'}, status= 400)

            if Signup.objects.filter(email = email).exists():
                return JsonResponse({'message': '이메일값이 중복되었습니다.'}, status= 401)
            
            if Signup.objects.filter(nickname = nickname).exists():
                return JsonResponse({'message': '닉네임값이 중복되었습니다.'}, status= 401)

            if Signup.objects.filter(phone_number = phone_number).exists():
                return JsonResponse({'message': '핸드폰번호가 중복되었습니다.'}, status= 401)
            
                
            
            Signup.objects.create(

            nickname     = nickname,
            email        = email,
            password     = password,
            phone_number = phone_number

            )
            
            
            return JsonResponse({'message': 'SUCCESS'}, status= 201)
            
        

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status= 400)
        
        

