import re
import json

from django.views import View
from django.http  import JsonResponse
from django.db.models   import Q 

from .models import User


class UserView(View):
    def post(self,request):
        try:
             data     = json.loads(request.body)
             mail     ='^[a-z0-9]+[\._]?[]+[@]\w+[.]\w{2,3}$'
             PASSWORD = 8
             if not re.search(mail, data['email']):
                 return JsonResponse({'MESSAGE':'EMAIL_KEY_ERROR'},status=400)
            
             if len(data['password']) <PASSWORD:
                return JsonResponse({'MESSAGE':'PASS_KEY_ERROR'},status=400)
                
             if User.objects.filter(
                Q(email = data['email'])| 
                Q(nickname = data['nickname'])|
                Q(phone_number=data['mobile'])):
    
                return JsonResponse({'MESSAGE':'USER_ALREADY_EXISIS'},status=400)

             User.objects.create(
                nickname       = data['nickname'],
                password       = data['password'],
                email          = data['email'],
                phone_number   = data['mobile']
            )
            
             return JsonResponse({'MESSAGE':'SUCCESS'}, status =201)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=400)

      

