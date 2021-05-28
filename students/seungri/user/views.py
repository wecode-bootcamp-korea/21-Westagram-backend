import json
import re

from django.views import View
from django.http  import JsonResponse
from django.db    import IntegrityError

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

            if re.compile(email_regex).match(email) == None:
                return JsonResponse({"message": "EMAIL_FORM_ERROR"}, status=400)
            if len(password) < 8 or len(password) > 15:
                return JsonResponse({"message": "PASSWORD_ERROR"}, status=400)

            User.objects.create(email     = email,
                                password  = password,
                                phone_num = phone_num,
                                nick_name = nick_name)
            return JsonResponse({"message": "SUCCESS!"}, status=201)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        except IntegrityError:
            return JsonResponse({"message": "DUPLICATE_ENTRY_KEY_ERROR"}, status=400)
