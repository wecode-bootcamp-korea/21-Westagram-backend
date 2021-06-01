import json, re, bcrypt, jwt

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q

from users.models import Account
from my_settings  import ALGORITHM, SECRET_KEY

class SignupView(View):
    def post(self, request):
        try:
            data         = json.loads(request.body)
            email        = data['email']
            password     = data['password']
            nickname     = data['nickname']
            phone_number = data['phone_number']

            EMAIL_REGEX    = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
            PASSWORD_REGEX = "^(?=.*).{8,}$"

            if not re.search(PASSWORD_REGEX, password):
                return JsonResponse({'message' : 'VALIDATION ERROR : INVALID PASSWORD'}, status=400)
            if not re.search(EMAIL_REGEX, email):
                return JsonResponse({'message' : 'VALIDATION ERROR : INVALID EMAIL'}, status=400)
            if Account.objects.filter(Q(email=email) | Q(nickname=nickname) | Q(phone_number=phone_number)).exists():
                return JsonResponse({'message' : 'USER INFORMATION ALREADY EXISTS'}, status=409)
            
            hashed_password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            Account.objects.create(
                email        = email,
                password     = hashed_password.decode('utf-8'),
                nickname     = nickname,
                phone_number = phone_number
            )
            return JsonResponse({'message' : 'SUCCESS!'}, status=201)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

class SigninView(View):
    def post(self, request):
        try:
            data           = json.loads(request.body)
            email          = data['email']
            input_password = data['password']
            user           = Account.objects.get(email = email)
            
            if not email or not input_password:
                return JsonResponse({'message' : 'KEY ERROR'}, status=400)
            if not Account.objects.filter(email=email).exists(): 
                return JsonResponse({'message' : 'INVALID USER'}, status=401)
            if not bcrypt.checkpw(input_password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message' : 'INVALID USER'}, status=401)

            email_data = {'email': email}
            token      = jwt.encode(email_data, SECRET_KEY, ALGORITHM)
            return JsonResponse({'message' : 'SUCCESS' , 'token' : token}, status=201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)  

