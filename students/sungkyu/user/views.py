import jwt, bcrypt, json, re

from django.views         import View
from django.http          import JsonResponse
from django.db.models     import Q

from westagram.settings   import SECRET_KEY
from .models              import User

class SignupView(View):
    def post(self, request):

        try:
            user_email            = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
            user_phone_number     = '^[0-9]{3}-[0-9]{4}-[0-9]{4}$'
            user_password         = '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,18}$'

            data                  = json.loads(request.body)
            
            # email과 password의 값이 들어있지 않은 경우
            # email과 password의 KEY값이 일치하지 않을 경우 keyerror 리턴
            if '' == data['email']:
                return JsonResponse({'message': 'INVALID_EMAI'}, status=400)

            if '' == data['password']:
                return JsonResponse({'message': 'INVALID_PASSWORD'}, status=400)

            # email과 password, phone_number가 정규표현식에 부합하지 않는 경우
            if not re.match(user_email, data['email']):
                return JsonResponse({'message': 'INVALID_EMAIL'}, status=400)

            if not re.match(user_phone_number, data['phone_number']):
                return JsonResponse({'message': 'INVALID_PHONE_NUMBER'}, status=400)

            if not re.match(user_password, data['password']):
                return JsonResponse({'message': 'INVALID_PASSWORD'}, status=400)

            # 중복검사
            if User.objects.filter(
                Q(email=data['email'])|
                Q(phone_number=data['phone_number'])|
                Q(nickname=data['nickname'])).exists():
                return JsonResponse({'MESSAGE' : 'OVERLAP_ERROR'}, status=400)

            # password 암호화
            password        = data['password'].encode('utf-8')
            password_bcrypt = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                email        = data['email'],
                password     = password_bcrypt,
                phone_number = data['phone_number'],
                nickname     = data['nickname'],
            )

            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

class SigninView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not User.objects.filter(email=data['email']).exists():
                return JsonResponse({"message": "INVALID_USER"}, status=401)
            user = User.objects.get(email=data['email'])

            # 비밀번호 확인
            if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                # 토큰 발행
                token = jwt.encode({'eamil' : data['email']}, SECRET_KEY, algorithm="HS256")
                return JsonResponse({"token": token}, status=200)
            else:
                return JsonResponse({"message": "INVALID_USER"},status=402)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
