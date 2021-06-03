import json, re, jwt, bcrypt

from django.views import View
from django.http import JsonResponse
from django.db.models import Q

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
            if SignUp.objects.filter(Q(email=data['email'])|Q(nickname=data['nickname'])).exists():
                return JsonResponse({"message":"wrong input!"},status = 400)

            #패스워드예외처리
            if  len(password) < 8:
                return JsonResponse({"message":"You should input more than 7 digits!"}, status = 400)

            #폰번호 예외처리
            if not len(phone_num) == 11:
                return JsonResponse({"message":"number of digits must be 11!"}) 

            SignUp.objects.create(
                email     = data['email'],
                password  = hashed_password.decode('utf-8'),
                phone_num = data['phone_num'],
                nickname  = data['nickname']
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
            email_password = SignUp.objects.get(email = data['email'])
            email_password = email_password.password 

            if not bcrypt.checkpw(password.encode('utf-8'),email_password.encode('utf-8')):
                return JsonResponse({"message":"Invalid password!"},status = 400)
            token = jwt.encode(email_data,SECRET_KEY,ALGORITHM)
    
            return JsonResponse({"message":token},status = 200)
        except KeyError:
                return JsonResponse({"message":"KEY_ERROR"},status = 400)
        except SignUp.DoesNotExist:
                return JsonResponse({"message":"Invalid_input"},status=400)
     

            
            

