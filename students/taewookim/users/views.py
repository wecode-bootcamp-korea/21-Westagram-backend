import json, re
from json.decoder           import JSONDecodeError

from django.views           import View
from django.http.response   import JsonResponse
from django.db.models       import Q

from .models                import User

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
            nickname     = data['nickname'] 
            phone_number = data['phone_number']

            if not re.match(EMAIL_REGEX, email):
                return JsonResponse({"message": "INVALIED_EMAIL"}, status=400)

            if not re.match(PASSWORD_REGEX, password):
                return JsonResponse({"message": "INVALIED_PASSWORD"}, status=400)

            if not re.match(NICKNAME_REGEX, nickname):
                return JsonResponse({"message": "INVALIED_NICKNAME"}, status=400)

            if not re.match(PHONE_REGEX, phone_number):
                return JsonResponse({"message": "INVALIED_PHONE_NUMBER"}, status=400)

            if User.objects.filter(
                Q(email=email) | 
                Q(nickname=nickname) | 
                Q(phone_number=phone_number)).exists() :
                return JsonResponse({"message": "DUPLICATED_INFORMATION"}, status=409)

            User.objects.create(
                email        = email,
                password     = password,
                phone_number = phone_number,
                nickname     = nickname
            )

            return JsonResponse({"message": "CREATED"}, status=201)

        except JSONDecodeError:
            return JsonResponse({"message": "EMPTY_BODY_DATA"}, status=400)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)