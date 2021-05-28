import json, re
from json.decoder           import JSONDecodeError

from django.views           import View
from django.http.response   import JsonResponse

from .models              import User

EMAIL_REGEX    = '^([a-z0-9_+.-]+@([a-z0-9-]+\.)+[a-z0-9]{2,4}){1,50}$'
PASSWORD_REGEX = '^.{8,30}$'
NICKNAME_REGEX = '^.{2,10}$'
PHONE_REGEX    = '^01[016789]\-\d{3,4}\-\d{4}$'

class UserView(View):
    def post(self, request):
        try:
            data         = json.loads(request.body)
            email        = data['email']
            password     = data['password']
            nickname     = data.get('nickname')
            phone_number = data.get('phone_number')

            if re.compile(EMAIL_REGEX).match(email) == None:
                return JsonResponse({"result": "INVALIED_EMAIL"}, status=400)

            if re.compile(PASSWORD_REGEX).match(password) == None:
                return JsonResponse({"result": "INVALIED_PASSWORD"}, status=400)

            if User.objects.filter(email=email).exists() :
                return JsonResponse({"result": "DUPLICATED_EMAIL"}, status=400)

            if nickname is not None:
                if not re.compile(NICKNAME_REGEX).match(nickname):
                    return JsonResponse({"result": "INVALIED_NICKNAME"}, status=400)

                if User.objects.filter(nickname=nickname).exists() :
                    return JsonResponse({"result": "DUPLICATED_NICKNAME"}, status=400)

            if phone_number is not None:
                if not re.compile(PHONE_REGEX).match(phone_number):
                    return JsonResponse({"result": "INVALIED_PHONE_NUMBER"}, status=400)

                if User.objects.filter(phone_number=phone_number).exists() :
                    return JsonResponse({"result": "DUPLICATED_PHONE_NUMBER"}, status=400)
                
            User.objects.create(email=email, password=password, phone_number=phone_number, nickname=nickname)

            return JsonResponse({"result": "CREATED"}, status=201)

        except JSONDecodeError:
            return JsonResponse({"result": "EMPTY_BODY_DATA"}, status=400)

        except KeyError:
            return JsonResponse({"result": "KEY_ERROR"}, status=400)