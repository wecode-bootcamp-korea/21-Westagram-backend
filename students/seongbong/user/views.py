import json

from django.http  import JsonResponse
from django.views import View 
from .models      import User 

class UserSignUp(View):
    def post(self, request):
        
        data = json.loads(request.body)
        if request.method == 'POST' and len(data['password']) < 8:
            return JsonResponse({'message': 'PASSWORD_ERROR'}, status= 400)
        if request.method == 'POST' and '@' '.' not in data['email']:
            return JsonResponse({'message': 'EMAIL_ERROR'}, status= 400)
        
        try:
            data = json.loads(request.body)
            User.objects.create(
                        email        = data['email'],
                        password     = data['password'],
                        nickname     = data['nickname'],
                        phone_number = data['phone_number']
                        )
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status= 400)

        return JsonResponse({'message': 'SUCCESS'}, status= 201)
        
    
