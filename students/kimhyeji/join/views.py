#from django.shortcuts import render
import json

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q

from .models import User

# Create your views here.

class JoinView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            if User.objects.filter(Q(password=data['password']) | Q(email=data['email'])):
                return JsonResponse({'message':'중복되었습니다.'}, status=400)

            if len(data['password']) < 8 :
                return JsonResponse({"message":"8자리이상입력하세요."}, status=400)

            if data['email'] in ('@' or '.') :
                return JsonResponse({"message":"이메일형식이잘못되었습니다."}, status=400)

            else:
                User.objects.create(
                    email        = data['email'],
                    phone_number = data.get('phone_number'),
                    password     = data['password'], 
                    nick_name    = data.get('nick_name')
                )
                return JsonResponse({'message':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

                        

            