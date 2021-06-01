import json, re

from django.views import View
from django.http  import JsonResponse
from django.db    import IntegrityError

from .models import User

email_regex = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if User.objects.filter(mobile=data['mobile']).exists():
                return JsonResponse({'massage': 'KEY_ERROR_MOBILE_EXIST'}, status=400)

            if User.objects.filter(nickname=data['nickname']).exists():
                return JsonResponse({'massage': 'KEY_ERROR_NICKNAME_EXIST'}, status=400)

            if not email_regex.match(data['email']):
                return JsonResponse({'message':'PLEASE ENTER @ or .'}, status=400)

            if len(data['password']) < 8:
                return JsonResponse({'massage': 'KEY_ERROR_PASSWORD'}, status=400)

            User.objects.create(
                email    = data['email'],
                password = data['password'],
                mobile   = data['mobile'],
                nickname = data['nickname']
            )
            
            return JsonResponse({'massage': 'SUCCESS'}, status=201)
        
        except KeyError:
            return JsonResponse({'massage': 'KEY_ERROR'}, status=400)
        
        except IntegrityError:
            return JsonResponse({'massage': 'KEY_ERROR_EMAIL_EXIST'}, status=400)
