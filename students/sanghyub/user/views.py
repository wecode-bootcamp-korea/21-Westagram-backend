import json
import re

from django.db.models.fields import EmailField
from django.views import View
from django.http  import JsonResponse, HttpResponse 
from django.core  import exceptions, validators

from .models      import User


regEXP_email = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
regEXP_pw    = re.compile(r'[a-zA-Z0-9+-_.]{8,}')
regEXP_phone = re.compile(r'\d{2,3}-\d{3,4}-\d{4}')


class UserSignUp(View) : 
    def post(self,request):
        try:
            data = json.loads(request.body)
            email        = data["email"]
            password     = data["password"]
            nickname     = data["nickname"]
            phone_number = data["phone_number"]

            if regEXP_email.match(email) and \
               regEXP_pw.match(password) and \
               regEXP_phone.match(phone_number):
               pass
            else:
                 return JsonResponse({"message":"IMPROPER input"}, status = 400)
          
            user = User.objects
                     
            if user.filter(email = email ).exists() or \
               user.filter(nickname = nickname ).exists() or \
               user.filter(phone_number = phone_number ).exists():
                 return JsonResponse({"message": "accout_info already exists"},status = 400)

            user.create(
                email        = email,
                password     = password,
                nickname     = nickname,
                phone_number = phone_number
            )
            return JsonResponse({"message": "CREATED!"}, status = 201)
        except KeyError:
            return JsonResponse({"message": "INVALID KEY"}, status = 400)
       

   


