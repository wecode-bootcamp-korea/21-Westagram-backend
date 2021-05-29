#from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views import View
from .models import Join
from django.db.models import Q

# Create your views here.

class JoinView(View):
    def post(self, request):
        data = json.loads(request.body)
        

        try:
           
            if Join.objects.filter(Q(password=data['password']) | Q(email=data['email'])):
          
                return JsonResponse({'message':'KEY_ERROR'}, status=400)

            if len(data['password']) < 8 :
                return JsonResponse({"message": "KEY_ERROR"}, status=400)

            if data['email'] in ('@' or '.') :
                return JsonResponse({"message": "KEY_ERROR"}, status=400)



            else:

                Join.objects.create(email = data['email'],phone_number = data['phone_number'],user_name = data['user_name'],password = data['password'], nick_name=data['nick_name'])

            return JsonResponse({'message':'SUCCESS'}, status=200)

        except KeyError:

            return JsonResponse({'message':'KEY_ERROR'}, status=400)

                        

            