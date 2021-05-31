import json
import re

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q

from .models import User

class UserView(View):
    def post(self, request):
        try:
            user_datas = json.loads(request.body)

            if user_datas['email'].replace(' ', '') == '':
                return JsonResponse({'result':'EMAIL_EMPTY'}, status=404)
            
            if not re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$').match(user_datas['email']):
                return JsonResponse({'result':'INVALID_EMAIL'}, status=404)

            if user_datas['password'].replace(' ', '') == '':
                return JsonResponse({'result':'EMPTY_PASSWORD'}, status=404)

            if len(user_datas['password']) < 8:
                return JsonResponse({'result':'INVALID_PASSWORD'}, status=404)
            
            if user_datas['phone_number'].replace(' ', '') == '':
                return JsonResponse({'result':'EMPTY_PHONE_NUMBER'}, status=404)

            if user_datas['full_name'].replace(' ', '') == '':
                return JsonResponse({'result':'EMPTY_FULL_NAME'}, status=404)
            
            if user_datas['user_name'].replace(' ', '') == '':
                return JsonResponse({'result':'EMPTY_USER_NAME'}, status=404)

            bValid = User.objects.filter(
                Q(email=user_datas['email']) | 
                Q(phone_number=user_datas['phone_number']) | 
                Q(user_name=user_datas['user_name'])
            ).exists()

            if bValid:
                return JsonResponse({'result':'DUPLICATE_KEY'}, status=404)
            
            User.objects.create(
                email        = user_datas['email'],
                password     = user_datas['password'],
                phone_number = user_datas['phone_number'],
                full_name    = user_datas['full_name'],
                user_name    = user_datas['user_name']
            )

            return JsonResponse({'result':'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'result':'INVALID_KEY'}, status=400)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'result':'INVALID_REQUEST_BODY'}, status=400)
