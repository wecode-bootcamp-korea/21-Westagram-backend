import json
import re

from django.views import View
from django.http  import JsonResponse
from django.db    import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from .models import User

class UserJoinIn(View):
    def post(self, request):
        try:
            data      = json.loads(request.body)
            email     = data["email"]
            password  = data["password"]
            phone_num = data["phone_num"]
            nick_name = data["nick_name"]
            
            email_regex = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

            if not re.match(email_regex, data['email']):
                return JsonResponse({"message": "EMAIL_FORM_ERROR"}, status =  400)

            if len(password) < 8 or len(password) > 15:
                return JsonResponse({"message": "PASSWORD_ERROR"}, status=400)

            User.objects.create(
                email     = email,
                password  = password,
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
            data      = json.loads(request.body)
            email     = data["email"]
            password  = data["password"]

            if email == "" or password == "":
                return JsonResponse({"message": "KEY_ERROR"}, status=400)
            elif User.objects.get(email=email, password=password):
                return JsonResponse({"message": "SUCCESS!"}, status=200)

        except ObjectDoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status=401)
