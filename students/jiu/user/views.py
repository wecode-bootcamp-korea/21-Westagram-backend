import json
import re

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q

from .models          import User


class NewUserView(View) :

    def post(self, request) :

        try:
            data = json.loads(request.body)

            re_email        = '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
            re_password     = '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,18}$'
            re_phone_number = '^[0-9]{3}[0-9]{4}[0-9]{4}$'

            # nickname, email, phone_number 중복 error
            if User.objects.filter(
                Q(nickname    =data['nickname']) or
                Q(email       =data['email'])    or
                Q(phone_number=data['phone_number'])
            ).exists() :
                return JsonResponse({'message':'ALREADY_EXISTS'}, status=400)

            # email address error ('@','.')
            if not re.match(re_email, data['email']) :
                return JsonResponse({'message':'WRONG_EMAIL_ERROR'}, status=400)
            
            # password min-length error ( 8 > len < 18 / 영문 대,소문자 , 숫자, 특수문자 조합)
            if not re.match(re_password, data['password'])  :
                return JsonResponse({'message':'PASSWORD_ERROR'}, status=400) 

            # phone_number (len == 11(3,4,4))
            if not re.match(re_phone_number, data['phone_number'])  :
                return JsonResponse({'message':'PHONE_NUMBER_ERROR'}, status=400) 

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

        

        


