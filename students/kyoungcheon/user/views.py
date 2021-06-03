import json
import re
import bcrypt
import jwt

from django.views    import View
from django.http     import JsonResponse
from django.db.utils import IntegrityError

from .models     import Member
from my_settings import SECRET_KEY

email_regex = "^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

class SignUp(View):
    def post(self, request):
        try:
            data          = json.loads(request.body)
            email_data    = data['email']
            password_data = data['password']
            phone_data    = data.get('phone')
            nickname_data = data.get('nickname')

            if len(password_data) < 8:
                return JsonResponse({'message': '비밀번호 8자이상 작성해주세요.'}, status=400)
            if not re.search(email_regex, email_data):
                return JsonResponse({'message': '이메일 형식에 맞게 작성해주세요.'}, status=400)
            if phone_data =='' or nickname_data =='':
                return JsonResponse({'message': "KEY_ERROR"}, status=400)

            hashed_password = bcrypt.hashpw(password_data.encode('UTF-8'), bcrypt.gensalt()).decode()

            Member.objects.create(
                email    = email_data,
                password = hashed_password,
                phone    = phone_data,
                nickname = nickname_data
                )

            return JsonResponse({'message': "SUCCESS","user_email":data['email']}, status=201)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        except IntegrityError as e:
            if email_data in str(e):
                return JsonResponse({'message':"이메일 중복입니다."}, status=409)
            if phone_data in str(e):
                return JsonResponse({'message':"핸드폰번호 중복입니다."}, status=409)
            if nickname_data in str(e):
                return JsonResponse({'message':"닉네임 중복입니다."}, status=409)

class SignIn(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_email = Member.objects.get(email=data['email'])

            if not Member.objects.filter(email=user_email.email).exists():
                return JsonResponse({'message':'INVALID_USER!!!!!'}, status=401)

            if not bcrypt.checkpw(data['password'].encode('utf-8'), user_email.password.encode('utf-8')):
                return JsonResponse({'message': 'INCORRECT_PASSWORD'}, status=402)
            access_token = jwt.encode({'id': user_email.id}, SECRET_KEY, algorithm='HS256')

            return JsonResponse({'token': access_token, 'message': 'SUCCESS','user_email':data['email']}, status=200)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)


