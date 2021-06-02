import json
import re
import jwt
import bcrypt
from django.views import View
from django.http import JsonResponse
from django.shortcuts import render
from .models import *
from my_settings import SECRET_KEY,ALGORITHM


# Create your views here.
class NewClient(View):
    def post(self,request):
        try:
            data      = json.loads(request.body)
            email     = data['email']
            password  = data['password']
            phone_num = data['phone_num']
            nickname  = data['nickname']
            hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
        
            #정규표현식
            if not re.match('[a-zA-Z0-9_-]+@[a-z]+.[a-z]+',email):
                return JsonResponse({"message":"You didn't match the right email foam!"},status = 400)
            if SignUp.objects.filter(email=data['email']).exists():
                return JsonResponse({"message":"Email already exists!"},status = 400)

            #패스워드예외처리
            if  len(password) < 8:
                return JsonResponse({"message":"You should input more than 7 digits!"}, status = 400)

            #폰번호 예외처리
            if not len(phone_num) == 11:
                return JsonResponse({"message":"number of digits must be 11!"}) 

            #닉네임 예외처리
            if SignUp.objects.filter(nickname=data['nickname']).exists():
                return JsonResponse({"message":"nickname already exists!"},status = 400)
            SignUp.objects.create(
                email=data['email'],
                password=hashed_password.decode('utf-8'),
                phone_num=data['phone_num'],
                nickname=data['nickname']
            )

            return JsonResponse({"message":"SUCCESS"},status = 201)
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"},status = 400)
        except TypeError:
            return JsonResponse({"message":"You should only input digits!"})

class Login(View):
    def post(self,request): 
        try:
            data      = json.loads(request.body)
            email     = data['email']
            password  = data['password']
            email_data     = {'email':data['email']}
            token          = jwt.encode(email_data,SECRET_KEY,ALGORITHM)

            p1 = SignUp.objects.get(email = data['email']).password #이메일을 가져와서 이메일에 해당하는 객체의 패스워드를 카리킴
           #p1은 스트링타입->encode를통해 바이트형으로 바꾼다
            if not bcrypt.checkpw(password.encode('utf-8'),p1.encode('utf-8')):#hashed password를 가져와서 클라이언트가 친 패스워드의 인코딩값을 비교한다
                return JsonResponse({"message":"Invalid password!"},status = 400)
            if not data['email'] or not data['password']: #exist() 필터 메소드의 하위 메소드 "email"이 스트링값이라
                #true false 로 판별 불가능// not 을 이용해 존재유무를 파악할수있다
                return JsonResponse({"message":"KEY_ERROR"},status = 400)
            
            # SignUp.objects.get(email=data['email'],password=data['password'],phone_num=data['phone_num'],nickname=data['nickname'])
            # 아이디생성하는것이 아니기때문에 create할필요가없음/ 확인만하고 넘어감
            return JsonResponse({"message":token},status = 200)
        except KeyError:
                return JsonResponse({"message":"KEY_ERROR"},status = 400)
        except SignUp.DoesNotExist:
                return JsonResponse({"message":"Invalid_input"},status=400)
     

            
            

