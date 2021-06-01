import json
import re

from django.views import View
from django.http import JsonResponse
from django.db.models import Q
from django.db import utils
from .models import User

class SignUpView(View):
    def post(self, request):
        try:
            data      = json.loads(request.body)
            email     = data['email']
            password  = data['password']
            phone_num = data.get('phone_num')
            name      = data.get('name')

            email_regex    = '^([\w\.\-_]+)?\w+@[\w]+(\.\w+){1,}$'
            password_regex = '^([a-zA-Z0-9~!@#$%^&*()_+]).{7,}$'

            if phone_num=='' or name=='':
                return JsonResponse({"message":"EMTPY_VALUE"}, status = 400)

            if not re.match(email_regex, email) or not re.match(password_regex, password) or not name or not phone_num:
                return JsonResponse({"message":"KEY_ERROR"}, status = 400)

            if User.objects.filter(Q(phone_num=phone_num)|Q(name=name)).exists():
                return JsonResponse({"message":"DUPLICATE_VALUEs"}, status = 409)

            User.objects.create(
                name      = name, 
                email     = email,
                phone_num = phone_num,
                password  = password
            )

            return JsonResponse({"result":"SUCCESS"}, status = 201)
            
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)

        except utils.IntegrityError:
            return JsonResponse({"message":"DUPLICATE_VALUE"}, status = 409)