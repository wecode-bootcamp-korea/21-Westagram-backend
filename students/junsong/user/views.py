import json, re
from json.decoder import JSONDecodeError

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q

from .models import User

class SignUp(View):
    def post(self, request):
        data     = json.loads(request.body)
        email    = data['email']
        password = data['password']
        nickname = data['nickname']
        contact  = data['contact']

        EMAIL_REGEX = '^([a-z0-9_+.-]+@([a-z0-9-]+\.)+[a-z0-9]{2,4}){1,128}$'

        try:
            if not re.match(EMAIL_REGEX, email):
                return JsonResponse({"message": "올바르지 않은 이메일 형식입니다."}, status=400)

            if len(password) < 8:
                return JsonResponse({"message": "비밀번호는 8자리 이상으로 만들어주세요."}, status=400)
                
            if User.objects.filter(Q(email=email)|Q(contact=contact)|Q(nickname=nickname)).exists():
                return JsonResponse({"message": "이미 존재하는 회원정보입니다."}, status=409)

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