import json,re

from django.views import View
from django.http import JsonResponse

from .models import User

class SignUpView(View):
    def post(self, request):
     
        data = json.loads(request.body)
        

        try:
            user_email = data['user_email']
            password   = data['password']
            phone      = data['phone']
            nickname   = data['nickname']
            
            validation_email = '^[A-Za-z0-9\.+_-]+\@[A-Za-z0-9\._-]+\.[a-zA-Z]+$' 

        
            if '' == user_email:
                return JsonResponse({'message': 'USER_ID_IS_EMPTY'}, status=400)
            if User.objects.filter(user_email = user_email).exists():
                return JsonResponse({'message': 'USER_ID_EXISTS'}, status=400)
            if not re.match (validation_email, user_email)  :
                return JsonResponse({'message': 'INVALID_EMAIL_FORMAT'}, status=400)
            if '' == password:
                return JsonResponse({'message': 'PASSWORD_IS_EMPTY'}, status=400)
            if len(password) < 8:
                return JsonResponse({'message': 'TOO_SHORT_PASSWORD'}, status=400) 
            if User.objects.filter(phone = phone).exists():
                return JsonResponse({'message': 'PHONE_NUMBER_EXISTS'}, status=400)
            if User.objects.filter(nickname = nickname).exists():
                return JsonResponse({'message': 'NICK_NAME_EXISTS'}, status=400) 
            
            
            else:
                User.objects.create(
                    user_email  = user_email,
                    password = password, 
                    phone    = phone,
                    nickname = nickname
                )
                return JsonResponse({'message': 'SUCCESS'} , status=201)
    
        except KeyError: 
            return JsonResponse({'message': 'KEY_ERROR'}, status=400) 
        except User.DoesNotExist:
            return JsonResponse ({'message':'USER_DOSE_NOT_EXIST'}, status=400)
        except Exception as e:
            return JsonResponse({"message": "UNKNOWN_ERROR"}, status=400)
        
            

    def get(self, request):
        user = User.objects.all()
        return JsonResponse({'user' : list(user)}, status = 200)
   