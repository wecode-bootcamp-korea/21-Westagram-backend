import jwt
import json
import bcrypt 

from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import ValidationError

from .models import User
from my_settings import SECRET_KEY, ALGORITHM

class NewUserView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            user = User(
                email        = data['email'], 
                password     = data['password'], 
                phone_number = data.get('phone_number'), 
                nickname     = data.get('nickname')
            )

            user.password     = self.make_hash_value(user.password)
            user.phone_number = self.check_blank(user.phone_number)
            user.nickname     = self.check_blank(user.nickname)
            
            user.full_clean()
            user.save()

            return JsonResponse({'message':'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        except ValidationError as e: 
            return JsonResponse({'message':e.message_dict}, status=400)

    def make_hash_value(self, value):
        result = bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        return result

    def check_blank(self, value):
        if value == "":
            return None
        else: 
            return value

class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            email    = data['email']
            password = data['password']

            user = User.objects.get(email=email)

            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message':'INVALID_USER'}, status=401)
            
            data = {'user_id':user.id}
            
            token = jwt.encode(data, SECRET_KEY, ALGORITHM)

            return JsonResponse({'access_token':token}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=401)
