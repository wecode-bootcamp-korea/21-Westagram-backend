import json
import re

from django.http import JsonResponse
from django.views import View

from users.models import Account

class SignupView(View):
    def post(self, request):
        MIN_PASSWORD_LENGTH = 8
        try:
            data = json.loads(request.body)
            email = data['email']
            password = data['password']
            nickname = data['nickname']
            phone_number = data['phone_number']

            if email and password:
                email_regex = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
                password_regex = "^(?=.*).{8,}$"
                if not re.search(password_regex, password):
                    return JsonResponse({'message' : 'VALIDATION ERROR : INVALID PASSWORD'}, status = 400)
                if not re.search(email_regex, email):
                    #@ 랑 . 은 email_regex에서 걸려서 구현 안해도 될것같은데 구현해놓긴 했습니다.
                    return JsonResponse({'message' : 'VALIDATION ERROR : INVALID EMAIL'}, status= 400 )
                if '@' not in email and '.' not in email:
                    return JsonResponse({'message' : 'Email does not include either ''@'' or ''.'' '}, status = 400)
                if len(password) < MIN_PASSWORD_LENGTH:
                    #마찬가지로 password_regex에서 걸려서 구현 안해도 될것같은데 문제에서 요구해서 하였습니다
                    return JsonResponse({'message' : 'VALIDATION ERROR : PASSWORD TOO SHORT'}, status =400)
                if Account.objects.filter(email=email).exists():
                    return JsonResponse({'message' : 'EMAIL ALREADY EXISTS'}, status = 400)
                if Account.objects.filter(nickname = nickname).exists():
                    return JsonResponse({'message' : 'NICKNAME ALREADY EXISTS'}, status = 400)
                if Account.objects.filter(phone_number = phone_number).exists():
                    return JsonResponse({'message' : 'PHONE NUMBER ALREADY EXISTS'}, status = 400)

                Account.objects.create(
                    email = email,
                    password = password,
                    nickname = nickname,
                    phone_number = phone_number
                )
                return JsonResponse({'message' : 'SUCCESS!'}, status =201)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

