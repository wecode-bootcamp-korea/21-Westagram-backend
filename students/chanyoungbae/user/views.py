import json
import re

from django.views import View
from django.http import JsonResponse
from .models import User

class SignUpView(View):
    def post(self, request):
        try:
            data      = json.loads(request.body)

            email     = data['email']
            password  = data['password']
            phone_num = data['phone_num']
            name      = data['name']

            email_regex    = '^([\w\.\-_]+)?\w+@[\w]+(\.\w+){1,}$'
            password_regex = '^([a-zA-Z0-9~!@#$%^&*()_+]).{7,}$'

            if not email or not password:
                return JsonResponse({"message": "KEY_ERROR"}, status = 400)

            if not re.match(email_regex, email):
                return JsonResponse({"message":"INVALID_VALUE"}, status = 400)

            if User.objects.filter(email=email):
                return JsonResponse({"message":"DUPLICATE EMAIL"}, status = 400)
            
            if phone_num:
                if User.objects.filter(phone_num=phone_num):
                    return JsonResponse({"message":"DUPLICATE PHONE NUMBER"}, status = 400)

            if name:    
                if User.objects.filter(name=name):
                    return JsonResponse({"message":"DUPLICATE NAME"}, status = 400)

            if not re.match(password_regex, password):
                return JsonResponse({"message":"SHORT PASSWORD"}, status = 400)
            
            User.objects.create(
                name      = name, 
                email     = email,
                phone_num = phone_num,
                password  = password
            )

            return JsonResponse({"result":"SUCCESS"}, status = 201)
            
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)