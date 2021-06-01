import json,re

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q

from .models          import User

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            email            = data['email']
            password         = data['password']
            phone            = data['phone']
            nickname         = data['nickname']   
            validation_email = '^\w+\@\w+\.\D+$'

            q = Q()

            if '' == email:
                return JsonResponse({'message': 'USER_ID_IS_EMPTY'}, status=400)
            if not re.match (validation_email, email):
                return JsonResponse({'message': 'INVALID_EMAIL_FORMAT'}, status=400)
            if '' == password:
                return JsonResponse({'message': 'PASSWORD_IS_EMPTY'}, status=400)
            if len(password) < 8:
                return JsonResponse({'message': 'TOO_SHORT_PASSWORD'}, status=400) 
            if User.objects.filter(Q(email = email) | Q(phone = phone) | Q(nickname = nickname)).exists():
                return JsonResponse({'message': 'ALREADY_EXISTS'}, status=400)
        
            User.objects.create(
                email    = email,
                password = password, 
                phone    = phone,
                nickname = nickname
            )
            return JsonResponse({'message': 'SUCCESS'}, status=201)
        except KeyError: 
            return JsonResponse({'message': 'KEY_ERROR'}, status=400) 
        except User.DoesNotExist:
            return JsonResponse ({'message':'USER_DOSE_NOT_EXIST'}, status=400)
       

    def get(self, request):
        user = User.objects.all()
        return JsonResponse({'user' : list(user)}, status = 200)
   