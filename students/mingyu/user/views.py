import re, json, bcrypt, jwt

from django.views import View
from django.http  import JsonResponse

from .models      import User
from my_settings  import SECRET_KEY, ALGORITHM

class SignupView(View):

    def post(self, request):
        try:
            data = json.loads(request.body)
            
            email_regex = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            password_regex = re.compile(r'[A-Za-z0-9@#$]{8,}')
            phone_number_regex = re.compile('\d{2,3}-\d{3,4}-\d{4}')
            
            if not email_regex.search(data['email']):
                return JsonResponse({"message" : "INVALID_EMAIL"}, status=400)

            if not password_regex.search(data['password']):
                return JsonResponse({'message': 'INVAILD_PASSWORD'})
        
            if not phone_number_regex.search(data['phone_number']):
                return JsonResponse({'message': 'INVALID_PHONE_NUMBER'})

            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            decode_password = hashed_password.decode('utf-8')
            
            User.objects.create (
                email        = data['email'],
                password     = decode_password,
                nickname     = data['nickname'],
                phone_number = data['phone_number']
            )

            return JsonResponse({'message': 'SUCCESS'}, status=201)
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class SigninView(View):

    def post(self, request):
        try:
            data = json.loads(request.body)

            email    = data['email']
            password = data['password']
            
            user_email = User.objects.get(email=email)
            
            if not User.objects.filter(email=email):
                return JsonResponse({'message': 'INVALID_USER'}, status=400)
            
            if not bcrypt.checkpw(password.encode('utf-8'), user_email.password.encode('utf-8')):
                return JsonResponse({'message': 'INVALID_USER'}, status=400)

            token = jwt.encode({'user-id': user_email.id}, SECRET_KEY,ALGORITHM)
            
            return JsonResponse({'token': token}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
            
        