import json
import re

from django.http      import JsonResponse
from django.views     import View

from .models import User
# Create your views here.

class UserView(View):
    def post(self, request):

        try:
            data = json.loads(request.body)
            email_regax  = "^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$" 

            if not re.match(email_regax, email=data['email']):
                return JsonResponse({"message":"이메일형식이잘못되었습니다."}, status=400)

            if User.objects.filter(email=data['email']).exist():
                return JsonResponse({'message':'중복되었습니다.'}, status=400)

            if len(data['password']) < 8 :
                return JsonResponse({"message":"8자리이상입력하세요."}, status=400)
   
            User.objects.create(
                    email        = data['email'],
                    phone_number = data.get('phone_number'),
                    password     = data['password'], 
                    nick_name    = data.get('nick_name')
                )
            return JsonResponse({'message':'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)


            