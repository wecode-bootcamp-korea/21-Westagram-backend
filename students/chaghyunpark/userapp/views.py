from json.decoder import JSONDecodeError
import re
import json
import jwt
import bcrypt

from django.views       import View
from django.http        import JsonResponse
from django.db.models   import Q 

from .models            import User
from my_settings        import SECRET_KEY,ALGORITHM



class SignView(View):
    def post(self,request):
        try:
             data     = json.loads(request.body)
             MAIL     ='^[a-z0-9]+[\._]?[]+[@]\w+[.]\w{2,3}$'
             PASSWORD = 8
             if not re.search(MAIL, data['email']):
                 return JsonResponse({'MESSAGE':'EMAIL_KEY_ERROR'},status=400)
            
             if len(data['password']) <PASSWORD:
                return JsonResponse({'MESSAGE':'PASS_KEY_ERROR'},status=400)
                
             if User.objects.filter(
                Q(email        = data['email'])| 
                Q(nickname     = data['nickname'])|
                Q(phone_number = data['mobile'])).exists():
    
                return JsonResponse({'MESSAGE':'USER_ALREADY_EXISIS'},status=400)
             User.objects.create(
                nickname       = data['nickname'],
                password       = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                email          = data['email'],
                phone_number   = data['mobile'])
            
             return JsonResponse({'MESSAGE':'SUCCESS'}, status =201)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=400)

      



class LoginView(View):
    def post(self,request):
        try:
            data       = json.loads(request.body)
            if not User.objects.filter(
            Q(email    = data['email'])|
            Q(password = data['password'])).exists():
                return JsonResponse ({"message": "아이디 혹은 비밀번호가 다릅니다."}, status=401)
            
            user_id = User.objects.get(email=data['email'])

            if not bcrypt.checkpw(data['password'].encode('utf-8'), user_id.password.encode('utf-8')):
                return JsonResponse({"message": "비밀번호 틀렸다."}, status=400 )

            a= jwt.encode({'email':data['email']},SECRET_KEY,ALGORITHM)
            return JsonResponse({'message':'성공했다','Token':a}, status=200)

        except KeyError :
            return JsonResponse({"message": "KEY_ERROR"}, status=400 )
        except ValueError:
            return JsonResponse({"message": "틀렸다"}, status=400 )



