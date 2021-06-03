import json, re, bcrypt, jwt

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q

from .models          import User
from my_settings      import SECRET_KEY, JWT_ALGORITHM

re_email    = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
re_password = '^[A-Za-z\d$@$!%^()*#?&]{8,}$'

class UserView(View):
    def post(self, request):
        try:
            data         = json.loads(request.body)
            user_name    = data['user_name']
            phone_number = data['phone_number']
            user_email   = data['user_email']
            password     = data['password']

            if not re.match(re_email, user_email):
                return JsonResponse({"message":"The email is not appropriate"}, status=400)

            if not re.match(re_password, password):
                return JsonResponse({"message":"The password is not appropriate"}, status=400)

            if User.objects.filter(
                Q(user_name    = user_name)|
                Q(phone_number = phone_number)|
                Q(user_email   = user_email)).exists():
                return JsonResponse({"message": "DUPLICATED_CLIENT_INFORMATION"}, status=409)

            hash_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                user_name    = user_name,
                phone_number = phone_number,
                user_email   = user_email,
                password     = hash_pw
            )
            return JsonResponse({'message':'SUCCESS'}, status = 201)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status = 400)

class LoginView(View):    
    def post(self,request):
        try:
            data       = json.loads(request.body)
            user_email = data['user_email']
            password   = data['password']
            
            if not User.objects.filter(user_email = user_email).exists():
                return JsonResponse({'message':'INVALID_USER'}, status = 401)
            
            user = User.objects.get(user_email = data['user_email'])
            
            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message':'PASSWORD INCORRECT!!'}, status = 401)
            
            return JsonResponse({'message':'LOGIN SUCCESS!!!',
                                   'Token': jwt.encode({'id':user.id}, SECRET_KEY, JWT_ALGORITHM)}, status = 200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR!!'}, status = 400)