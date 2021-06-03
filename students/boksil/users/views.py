import json, re, jwt, bcrypt

from django.views import View
from django.http  import JsonResponse
from django.db    import IntegrityError

from .models            import User
from westagram.settings import SECRET_KEY, ALGORITHM

email_regex = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

class SignupView(View):
    def post(self, request):
        try:
            data            = json.loads(request.body)
            bcrypt_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            if User.objects.filter(mobile=data['mobile']).exists():
                return JsonResponse({'massage': 'MOBILE_EXIST'}, status=400)

            if User.objects.filter(nickname=data['nickname']).exists():
                return JsonResponse({'massage': 'NICKNAME_EXIST'}, status=400)

            if not email_regex.match(data['email']):
                return JsonResponse({'message':'PLEASE ENTER @ or .'}, status=400)

            if len(data['password']) < 8:
                return JsonResponse({'massage': 'PASSWORD OF LEAST 8 CHARACTERS'}, status=400)

            User.objects.create(
                email    = data['email'],
                password = bcrypt_password,
                mobile   = data['mobile'],
                nickname = data['nickname']
            )
            
            return JsonResponse({'massage': 'SUCCESS'}, status=201)
        
        except KeyError:
            return JsonResponse({'massage': 'KEY_ERROR'}, status=400)
        
        except IntegrityError:
            return JsonResponse({'massage': 'INTEGRITY_ERROR'}, status=400)

class SigninView(View):
    def post(self, request):
        try: 
            data           = json.loads(request.body)
            input_email    = data['email']
            input_password = data['password'].encode('utf-8')

            if input_email == '' or input_password == '':
                return JsonResponse({'message': 'INVALID_USER'}, status=401)

            db_email    = User.objects.get(email=input_email)
            db_password = db_email.password.encode('utf-8') # 가져온 이메일의 패스워드를 다시 encode

            if not bcrypt.checkpw(input_password, db_password):
                return JsonResponse({'message': 'INVALID_USER'}, status=401)
            
            token = jwt.encode({'user_id': db_email.id}, SECRET_KEY, ALGORITHM)

            return JsonResponse({'token': token, 'message': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'massage': 'KEY_ERROR'}, status=400)
        