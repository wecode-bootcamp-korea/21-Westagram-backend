import re
import json
import bcrypt

from django.views import View
from django.http  import JsonResponse, request
from django.db.models   import Q 

from .models import User


class UserView(View):
    def post(self,request):
        try:
             data     = json.loads(request.body)
             mail     ='^[a-z0-9]+[\._]?[]+[@]\w+[.]\w{2,3}$'
             PASSWORD = 8
             if not re.search(mail, data['email']):
                 return JsonResponse({'MESSAGE':'EMAIL_KEY_ERROR'},status=400)
            
             if len(data['password']) <PASSWORD:
                return JsonResponse({'MESSAGE':'PASS_KEY_ERROR'},status=400)
                

             if User.objects.filter(
                Q(email        = data['email'])| 
                Q(nickname     = data['nickname'])|
                Q(phone_number = data['mobile'])).exists():
    
                return JsonResponse({'MESSAGE':'USER_ALREADY_EXISIS'},status=400)
            #  hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'),bcrypt.gensalt()).decode()
             User.objects.create(
                nickname       = data['nickname'],
                password       = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                email          = data['email'],
                phone_number   = data['mobile'])
            
             return JsonResponse({'MESSAGE':'SUCCESS'}, status =201)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=400)

      



class LogView(View):
    def post(self,request):
        try:
            data = json.loads(request.body)
            if not User.objects.filter(
            Q(email    = data['email'])|
            Q(password = data['password'])).exists():
                return JsonResponse ({"message": "INVALID_USER."}, status=401)
            
            user_id =User.objects.get(email=data['email'])

            if User.objects.filter(email=data['email']):
                if bcrypt.checkpw(data['password'].encode('utf-8'), user_id.password.encode('utf-8')):
                    return JsonResponse({'message':'성공했다'}, status=200)
                        
        except KeyError :
            return JsonResponse({"message": "KEY_ERROR"}, status=400 )




# http POST localhost:8000/userapp/user nickname='도곡동노' password='q' email='chsk@naver.com' mobile='010-563-2354'
