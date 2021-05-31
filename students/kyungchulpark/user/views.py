import json
import bcrypt
import jwt

from django.core.exceptions import ValidationError

from django.http  import JsonResponse
from django.views import View
from .models      import User
from .validators  import validate_phone, validate_email, validate_password, validate_nickname
from my_settings  import SECRET_KEY

class UserView(View):
    def post(self,request):
        try:
            data = json.loads(request.body)
        
            email_data        = data['email'] 
            password_data     = data['password'] 
            nickname_data     = data['nickname'] 
            phone_number_data = data['phone_number'] 
            
            validate_email(email_data)
            validate_password(password_data)
            validate_phone(phone_number_data)
            validate_nickname(nickname_data)

            hased_password   = bcrypt.hashpw(password_data, bcrypt.gensalt())

            User.objects.create(
                email        = email_data,
                password     = hased_password,
                nickname     = nickname_data,
                phone_number = phone_number_data)

            return JsonResponse({'result':'SUCCESS'}, status=201)
        
        except KeyError:
            return JsonResponse({'message':'INVALID_KEY'}, status=400)
        except ValidationError as e:
            return JsonResponse({'message':str(e)}, status=400)
    
    
class LoginView(View):   
    def post(self,request):
        try:
            data = json.loads(request.body)

            email_data    = data['email']
            password_data = data['password']

            user = User.objects.get(email=email_data)
            
            if user.email == None:
                return JsonResponse({'message':'INVALID_USER'}, status=401)
            if not bcrypt.checkpw(password_data, user.password):
                return JsonResponse({'message':'INVALID_USER'}, status=401)
            else:
                SECRET = SECRET_KEY
                access_token = jwt.encode({'id':user.id}, SECRET, algorithm='HS256')
                
                return JsonResponse({'message':'SUCCESS', 'access_token':access_token}, status=200)            

        except KeyError:
            return JsonResponse({'message':'INVALID_KEY'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=401)
