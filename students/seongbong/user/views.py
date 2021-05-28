import json, re

from django.http  import JsonResponse
from django.db    import IntegrityError
from django.views import View 
from .models      import User 

email_regex = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

class UserSignUp(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            if request.method == 'POST' and len(data['password']) < 8:
                return JsonResponse({'message': 'PASSWORD_ERROR'}, status= 400)
            
            if not re.compile(email_regex).match(data['email']):
                return JsonResponse({'message': 'EMAIL_ERROR'}, status= 400)   
            User.objects.create(
                        email        = data['email'],
                        password     = data['password'],
                        nickname     = data['nickname'],
                        phone_number = data['phone_number']
                        )
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status= 400)
        except IntegrityError:
            return JsonResponse({'message': 'UNIQUE_ERROR'}, status= 400)
        
        return JsonResponse({'message': 'SUCCESS'}, status= 201)
        
    
