import re
import json
from django.db.models.fields import related
from django.views import View
from django.http import JsonResponse 
from .models import User




class UserView(View):
    def post(self,request):
        data = json.loads(request.body)
        regex ='^[a-z0-9]+[\._]?[]+[@]\w+[.]\w{2,3}$'
        PASSWORD = 8

        
        try:
            if not (re.search(regex, data['email'])):
                return JsonResponse({'MESSAGE':'EMAIL_KEY_ERROR'},status=400)
            
            if len(data['password']) <PASSWORD:
                return JsonResponse({'MESSAGE':'PASS_KEY_ERROR'},status=400)
            
            if User.objects.filter(email=data['email']):
                return JsonResponse({'MESSAGE':'USER_ALREADY_EXISIS'},status=400)
            
            if User.objects.filter(nicname=data['nicname']):
                return JsonResponse({'MESSAGE':'USER_ALREADY_EXISIS'},status=400)

 
            user = User.objects.create(
                nickname       = data['name'],
                password       = data['password'],
                email          = data['email'],
                phone_number   = data['mobile']
            )
            
            return JsonResponse({'MESSAGE':'SUCCESS'}, status =201)

            
            
        except:
            return JsonResponse({'message':'SUCCESS!'},status=200)

      
    
