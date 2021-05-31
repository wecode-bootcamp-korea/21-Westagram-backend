import json, re, bcrypt, jwt
from json.decoder            import JSONDecodeError

from django.views            import View
from django.http.response    import JsonResponse
from django.db.models        import Q

from .models                 import User
from westagram.settings      import SECRET_KEY, HASH_ALGORITHM

EMAIL_REGEX    = '^([a-z0-9_+.-]+@([a-z0-9-]+\.)+[a-z0-9]{2,4}){1,50}$'
PASSWORD_REGEX = '^.{8,30}$'
NICKNAME_REGEX = '^.{2,10}$'
PHONE_REGEX    = '^01[016789]\-\d{3,4}\-\d{4}$'

def encrypt_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

def make_user_token(id):
    return jwt.encode({'user_id': id}, SECRET_KEY, algorithm=HASH_ALGORITHM)

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
                password     = encrypt_password(password),
                phone_number = phone_number,
                nickname     = nickname
            )

            return JsonResponse({"message": "CREATED"}, status=201)

        except JSONDecodeError:
            return JsonResponse({"message": "EMPTY_BODY_DATA"}, status=400)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

class LoginView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']
            user     = User.objects.get(email=email)

            if not check_password(password, user.password):
                return JsonResponse({"message": "INVALID_USER"}, status=401)

            return JsonResponse({"message": "SUCCESS",
                                 "token"  : make_user_token(user.id)}, status=200)

        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status=401)
        
        except JSONDecodeError:
            return JsonResponse({"message": "EMPTY_BODY_DATA"}, status=400)

        except KeyError:
            return JsonResponse({"result": "KEY_ERROR"}, status=400)