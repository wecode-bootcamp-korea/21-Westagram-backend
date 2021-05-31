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
            email1        = data["email"]
            password1     = data["password"]
            nickname1     = data["nickname"]
            phone_number1 = data["phone_number"]


            if regEXP_email.match(email1) and \
               regEXP_pw.match(password1) and \
               regEXP_phone.match(phone_number1):
               pass
            else:
                 return JsonResponse({"message":"IMPROPER input"}, status = 400)
          

            user = User.objects
                     
            if user.filter(email = email1 ).exists() or \
               user.filter(nickname = nickname1 ).exists() or \
               user.filter(phone_number = phone_number1 ).exists():
                 return JsonResponse({"message": "accout_info already exists"},status = 400)

            user.create(
                email        = email1,
                password     = password1,
                nickname     = nickname1,
                phone_number = phone_number1
            )
            
            return JsonResponse({"message": "CREATED!"}, status = 201)
        except KeyError:
            return JsonResponse({"message": "INVALID KEY"}, status = 400)
       

   


