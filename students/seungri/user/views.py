import json, re, bcrypt, jwt

from django.views import View
from django.http  import JsonResponse
from django.db    import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from westagram.settings import SECRET_KEY, ALGORITHM
from .models import User

class UserJoinIn(View):
    def post(self, request):
        try:
            data      = json.loads(request.body)
            email     = data['email']
            password  = data['password']
            phone_num = data['phone_num']
            nick_name = data['nick_name']
            
            email_regex = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

            if not re.match(email_regex, data['email']):
                return JsonResponse({"message": "EMAIL_FORM_ERROR"}, status =  400)

            if len(password) < 8 or len(password) > 15:
                return JsonResponse({"message": "PASSWORD_ERROR"}, status=400)

            User.objects.create(
                email     = email,
                password  = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                phone_num = phone_num,
                nick_name = nick_name
                )
            return JsonResponse({"message": "SUCCESS!"}, status=200)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        except IntegrityError:
            return JsonResponse({"message": "DUPLICATE_ENTRY_KEY_ERROR"}, status=400)

class UserLogIn(View):
    def post(self, request):
        try:
            data            = json.loads(request.body)
            email           = data['email']
            input_password  = data['password'].encode('utf-8')

            if email == "" or input_password == "":
                return JsonResponse({"message": "KEY_ERROR"}, status=400)

            login_user  = User.objects.get(email=email)
            db_password = login_user.password.encode('utf-8')
            
            if not bcrypt.checkpw(input_password, db_password):  
                return JsonResponse({"message": "INVALID_USER"}, status=401)

            token     = jwt.encode({"user_id" : login_user.id}, SECRET_KEY, algorithm=ALGORITHM)
            return JsonResponse({"token" : token, "message" : "SUCCESE!"}, status=200)

        except ObjectDoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status=401)


