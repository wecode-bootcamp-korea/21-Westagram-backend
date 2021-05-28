import json
import re
from django.db.models.fields import EmailField

from django.views import View
from django.http  import JsonResponse, HttpResponse 
from django.core  import exceptions, validators

from .models      import User


regEXP_email = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
regEXP_pw    = re.compile('[a-zA-Z0-9+-_.]{8,}')


class UserSignIn(View) : 
    def post(self,request):
        try:
            data = json.loads(request.body)

            if regEXP_email.match(data["email"]) == None or regEXP_pw.match(data["password"]) == None:
                return JsonResponse({"message":"IMPROPER input"}, status= 400)
            
            for person in User.objects.all():
                if data["email"] == person.email or data["name"] == person.name or data["phone_number"] == person.phone_number:
                    return JsonResponse({"message": "accout_info already exists"},status=400)

            User.objects.create(
                email        = data['email'],
                password     = data['password'],
                nickname     = data['nickname'],
                phone_number = data['phone_number']
            )
            
            return JsonResponse({"message": "CREATED!"}, status=201)
        except KeyError:
            return JsonResponse({"message": "INVALID KEY"},status=400)
       

   


