import json
import re

from django.http import JsonResponse
from django.views import View
from django.db.models import Q

from users.models import Account

class SignupView(View):
    def post(self, request):
        MIN_PASSWORD_LENGTH = 8
        try:
            data            = json.loads(request.body)
            email           = data['email']
            password        = data['password']
            nickname        = data['nickname']
            phone_number    = data['phone_number']

            email_regex     = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
            password_regex  = "^(?=.*).{8,}$"

            if not re.search(password_regex, password):
                return JsonResponse({'message' : 'VALIDATION ERROR : INVALID PASSWORD'}, status=400)
            if not re.search(email_regex, email):
                return JsonResponse({'message' : 'VALIDATION ERROR : INVALID EMAIL'}, status=400)
            if Account.objects.filter(Q(email=email) | Q(nickname=nickname) | Q(phone_number=phone_number)).exists():
                return JsonResponse({'message' : 'USER INFORMATION ALREADY EXISTS'}, status=400)

            Account.objects.create(
                email           = email,
                password        = password,
                nickname        = nickname,
                phone_number    = phone_number
            )
            return JsonResponse({'message' : 'SUCCESS!'}, status=201)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

