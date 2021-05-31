import json
from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q
from .models          import User


class NewUserView(View) :

    def post(self, request) :

        try:
            data = json.loads(request.body)
  
            # nickname, email, phone_number 중복 error
            if User.objects.filter(
                Q(nickname    =data['nickname']) or
                Q(email       =data['email'])    or
                Q(phone_number=data['phone_number'])
            ).exists() :
                return JsonResponse({'message':'ALREADY_EXISTS'}, status=400)

            # email address error ('@','.')
            if '@' not in data['email'] or '.' not in data['email'] :
                return JsonResponse({'message':'WRONG_EMAIL_ERROR'}, status=400)
            
            # password min-length error (len < 8)
            if 8 > len(data['password'])  :
                return JsonResponse({'message':'PW_MINLENGTH_ERROR'}, status=400) 

            # create
            User.objects.create(
                nickname    =data['nickname'],
                email       =data['email'],
                password    =data['password'],
                phone_number=data['phone_number']
                )
            return JsonResponse({'message':'SUCCESS'}, status=201)

            
        except KeyError :
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        

        


