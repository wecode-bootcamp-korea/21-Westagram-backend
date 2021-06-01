import json, re

from django.http  import JsonResponse
from django.db    import IntegrityError
from django.views import View 
from .models      import User 

class UserSignUp(View):
    def post(self, request):
        email_regex = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        data = json.loads(request.body)
        signup_data = User.objects.all()
        try:
            if not re.match(email_regex, data['email']):
                return JsonResponse({'message': 'EMAIL_ERROR'}, status=400) 
            
            if len(data['password']) < 8:
                return JsonResponse({'message': 'PASSWORD_ERROR'}, status=400)
            
            if signup_data.filter(nickname = data['nickname']).exists(): 
                return JsonResponse({'message': 'UNIQUE_ERROR'}, status=400)

            if signup_data.filter(phone_number = data['phone_number']).exists():
                return JsonResponse({'message': 'UNIQUE_ERROR'}, status=400)    

            User.objects.create(
                email        = data['email'],
                password     = data['password'],
                nickname     = data['nickname'],
                phone_number = data['phone_number']
            )
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except IntegrityError:
            return JsonResponse({'message': 'UNIQUE_ERROR'}, status=400)
        
        return JsonResponse({'message': 'SUCCESS'}, status=201)
        
    



