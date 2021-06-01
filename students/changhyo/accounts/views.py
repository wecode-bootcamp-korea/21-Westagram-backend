import json
import re
from django.views import View
from django.http import JsonResponse
from django.shortcuts import render
from .models import *

# Create your views here.
class NewClient(View):
    def post(self,request):
        try:
            data = json.loads(request.body)
            email     = data['email']
            password  = data['password']
            phone_num = data['phone_num']
            nickname  = data['nickname']
            input_validation = False
        
            #정규표현식
            p = re.compile('[a-zA-Z0-9_-]+@[a-z]+.[a-z]+')
            
            if not p.match(email):
                return JsonResponse({"message":"You didn't match the right email foam!"},status = 400)
            if SignUp.objects.filter(email=data['email']).exists():
                return JsonResponse({"message":"Email already exists!"},status =400)
            #패스워드예외처리
            if  len(password)<8:
                return JsonResponse({"message":"You should input more than 7 digits!"}, status = 400)

            #폰번호 예외처리
            if len(phone_num) == 11:
                try:
                    num = re.compile('\d{3}\d{3,4}\d{4}')
                    num.match(phone_num)
                except TypeError:
                    return JsonResponse({"message":"You should only input digits!"})
            else:
                return JsonResponse({"message":"number of digits must be 11!"}) 

            #닉네임 예외처리
            if SignUp.objects.filter(nickname=data['nickname']).exists():
                return JsonResponse({"message":"nickname already exists!"},status = 400)
            SignUp.objects.create(email=data['email'],password=data['password'],phone_num=data['phone_num']
            ,nickname=data['nickname'])

            return JsonResponse({"message":"SUCCESS"},status =201)
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"},status = 400)
            
            

