import json
import re
import bcrypt
import jwt

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q
from django.db        import utils

from .models     import User
from my_settings import SECRET_KEY, ALGORITHM

class SignUpView(View):
    def post(self, request):
        try:
            data      = json.loads(request.body)
            email     = data['email']
            password  = data['password']
            phone_num = data['phone_num']
            name      = data['name']
            en_pw     = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


            email_regex    = '^([\w\.\-_]+)?\w+@[\w]+(\.\w+){1,}$'
            password_regex = '^([a-zA-Z0-9~!@#$%^&*()_+]).{7,}$'

            if phone_num=='' or name=='':
                return JsonResponse({"message":"EMTPY_VALUE"}, status = 400)

            if not re.match(email_regex, email) or not re.match(password_regex, password) or not name or not phone_num:
                return JsonResponse({"message":"KEY_ERROR"}, status = 400)

            if User.objects.filter(Q(phone_num=phone_num)|Q(name=name)).exists():
                return JsonResponse({"message":"DUPLICATE_VALUE"}, status = 409)

            User.objects.create(
                name      = name, 
                email     = email,
                phone_num = phone_num,
                password  = en_pw.decode('utf-8')
            )

            return JsonResponse({"result":"SUCCESS"}, status = 201)
            
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)

        except utils.IntegrityError:
            return JsonResponse({"message":"DUPLICATE_VALUE"}, status = 409)

class SignInView(View):
    def post(self, request):
        try:
            data       = json.loads(request.body)
            email      = data['email']
            password   = data['password']
            email_dic  = {"email":email}
            en_pass    = password.encode('utf-8')
            en_db_pass = User.objects.get(email=email).password.encode('utf-8')
            
            if not bcrypt.checkpw(en_pass,en_db_pass):
                return JsonResponse({"message":"INVALID_USER"}, status = 401)

            token = jwt.encode(email_dic, SECRET_KEY, ALGORITHM)

            return JsonResponse({"Token":token}, status = 201)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)
        
        except User.DoesNotExist:
            return JsonResponse({"message":"INVALID_USER"}, status = 401)
