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
            data = json.loads(request.body)#data 는 딕셔너리의 형태로 클라이언트의 정보를 받는다
            email     = data['email']#브래킷안의 문자열은 딕셔너리의 키값을 의미하고 해당키의 값(data['email'])은 변수로 받는다(email) 
            password  = data['password']#해당값은 클라이언트가 입력한다
            phone_num = data['phone_num']
            nickname  = data['nickname']
            input_validation = False
            # for i in email:
            #     if '@' in i:
            #         return JsonResponse({"message":"Input @"},status = 400)
            #     elif '.' in i:
            #         return JsonResponse({"message":"Input ."},status = 400)
            #     else:
            #         break

            #이메일예외처리
            #정규표현식x email 스트링에 골뱅이가 있는지 조건문으로 

            if len(email) == input_validation:
                suffix = ".com"
                if len(email)>300:
                    return JsonResponse({"message":"You extended maximum range!"},status = 400)

                if email.counts("@") == 1:
                    try:
                        email.endswith(suffix)
                    except EOFError:
                        return JsonResponse({"mesasge":"Email should end with .com !"})
                else:
                    return JsonResponse({"message":"Input one @ !"},status = 400)
                
                #정규표현식
                p = re.compile("[0-9a-zA-Z]+(.[_a-z0-9-]+)*@(?:\\w+\\.)+\\w+$")
                if p.match(email) == input_validation:
                    return JsonResponse({"message":"You didn't match the right email form!"},status = 400)
            else:
                return JsonResponse({"mesasge":"email already exists!"},status = 400)

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
                pass
            else:
                return JsonResponse({"message":"nickname already exists!"},status = 400)
            
            SignUp.objects.create(email= data['email'],password = data['password'],phone_num = data['phone_num'],
            nickname=data['nickname'])#create 안에는 밸류 = 키형태로 써준다

            return JsonResponse({"message":"SUCCESS"},status =201)
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"},status = 400)
            #views.py는 단지 서버와의 통신을 위한것이라서 셸에서 객체를 생성하거나 정보를 불러올때는 모델파일의 클래스를 이용한다
            

