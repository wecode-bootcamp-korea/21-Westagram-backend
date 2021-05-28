import json
from json.decoder import JSONDecodeError

from django.views import View
from django.http  import JsonResponse

from .models import User

class SignUp(View):
    def post(self, request):
        data     = json.loads(request.body)
        email    = data['email']
        password = data['password']
        nickname = data['nickname']
        contact  = data['contact']

        try:
            if ('@' or '.') not in email:
                return JsonResponse({"message": "올바르지 않은 이메일 형식입니다."}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"message": "이미 존재하는 계정입니다."}, status=409)

            if len(password) < 8:
                return JsonResponse({"message": "비밀번호는 8자리 이상으로 만들어주세요."}, status=400)

            if (contact != '') and User.objects.filter(contact=contact).exists():
                return JsonResponse({"message": "중복된 연락처입니다."}, status=409)

            if (nickname != '') and User.objects.filter(nickname=nickname).exists():
                return JsonResponse({"message": "중복된 닉네임입니다."}, status=409)

            else:
                User.objects.create(
                    email    = email,
                    password = password,
                    nickname = nickname,
                    contact  = contact
                )
                return JsonResponse({"message": "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        
        except JSONDecodeError:
            return JsonResponse({"message": "EMPTY_BODY_DATA"}, status=400)