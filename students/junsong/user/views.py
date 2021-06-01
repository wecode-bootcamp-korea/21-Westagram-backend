import json, re, bcrypt, jwt
from json.decoder import JSONDecodeError

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q

from my_settings import SECRET_KEY
from .models     import User

class SignUp(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
            nickname = data['nickname']
            contact  = data['contact']
            password = data['password']

            password_crypt = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            EMAIL_REGEX = '^([a-z0-9_+.-]+@([a-z0-9-]+\.)+[a-z0-9]{2,4}){1,128}$'

            if not re.match(EMAIL_REGEX, email):
                return JsonResponse({"message": "올바르지 않은 이메일 형식입니다."}, status=400)

            if len(password) < 8:
                return JsonResponse({"message": "비밀번호는 8자리 이상으로 만들어주세요."}, status=400)
                
            if User.objects.filter(Q(email=email)|Q(contact=contact)|Q(nickname=nickname)).exists():
                return JsonResponse({"message": "이미 존재하는 회원정보입니다."}, status=409)

            User.objects.create(
                email    = email,
                password = password_crypt,
                nickname = nickname,
                contact  = contact
            )
            return JsonResponse({"message": "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        
        except JSONDecodeError:
            return JsonResponse({"message": "EMPTY_BODY_DATA"}, status=400)

class SignIn(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']

            EMAIL_REGEX = '^([a-z0-9_+.-]+@([a-z0-9-]+\.)+[a-z0-9]{2,4}){1,128}$'

            if not re.match(EMAIL_REGEX, email):
                return JsonResponse({"message": "올바르지 않은 이메일 형식입니다."}, status=400)
            
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                    token = jwt.encode({'user_email': email}, SECRET_KEY, algorithm='HS256')
                    return JsonResponse({"message": "SUCCESS", "token": token}, status=200)

            return JsonResponse({"message": "INVALID_USER"}, status=401)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        
        except JSONDecodeError:
            return JsonResponse({"message": "EMPTY_BODY_DATA"}, status=400)