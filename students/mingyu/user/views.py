import re
import json

from django.views import View
from django.http  import JsonResponse

from .models      import User

class SignupView(View):

    def post(self, request):
        try:
            data = json.loads(request.body)
            
            email_regex = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

            if not email_regex.search(data['email']):
                return JsonResponse({"message" : "INVALID_EMAIL"}, status=400)

            password_regex = re.compile(r'[A-Za-z0-9@#$]{8,}')

            if not password_regex.search(data['password']):
                return JsonResponse({'message': 'INVAILD_PASSWORD'})
            
            User.objects.create (
                email        = data['email'],
                password     = data['password'],
                nickname     = data['nickname'],
                phone_number = data['phone_number']
                )

            return JsonResponse({'message': 'SUCCESS'}, status=201)
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
