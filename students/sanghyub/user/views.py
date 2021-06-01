import json
import re
import bcrypt
import jwt
import os
import sys
sys.path.append(os.path.dirname('/Users/mac/Desktop/wecode_dev/21-Westagram-backend/students/sanghyub/21-Westagram-backend/students/sanghyub'))

from django.db.models.fields import EmailField
from django.views import View
from django.http  import JsonResponse, HttpResponse 
from django.core  import exceptions, validators

from .models      import User
from sanghyub.my_settings import SECRET_KEY

regEXP_email = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
regEXP_pw    = re.compile(r'[a-zA-Z0-9+-_.]{8,}')
regEXP_phone = re.compile(r'\d{2,3}-\d{3,4}-\d{4}')

SECRET = SECRET_KEY


class UserSignUp(View) : 
    def post(self,request):
        try:
            data = json.loads(request.body)
            email        = data["email"]
            password     = data["password"]
            nickname     = data["nickname"]
            phone_number = data["phone_number"]
            
            if regEXP_email.match(email) and \
               regEXP_pw.match(password) and \
               regEXP_phone.match(phone_number) :
               pass
            else:
               return JsonResponse({"message":"IMPROPER input"}, status = 400)
           
            user = User.objects 
            if user.filter(email = email ).exists() or \
               user.filter(nickname = nickname ).exists() or \
               user.filter(phone_number = phone_number ).exists():
                 return JsonResponse({"message": "accout_info already exists"},status = 400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
            decode_hash_pw  = hashed_password.decode('utf-8')
        
            user.create(
                email        = email,
                password     = decode_hash_pw,
                nickname     = nickname,
                phone_number = phone_number
            )
            return JsonResponse({"message": "CREATED!"}, status = 201)
        except KeyError:
            return JsonResponse({"message": "INVALID KEY"}, status = 400)


class UserSignIn(View) : 
    def post(self,request):
        try:
            data        = json.loads(request.body)
            signin_user = User.objects.get(email = data["email"])
        
            if bcrypt.checkpw(data['password'].encode("utf-8"),
                              signin_user.password.encode('utf-8')):            
                access_token = jwt.encode({'id':signin_user.id},
                                            SECRET,
                                            algorithm = 'HS256')
                user_info = [{"token":access_token}]
                return JsonResponse({"message": user_info}, status = 200)  
            else:
                return JsonResponse({"message":"INVALID_USER"}, status = 400)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEY"},status = 400)
        except exceptions.ObjectDoesNotExist:
            return JsonResponse({"message":"INVALID_USER"}, status = 404)

    class UserPost(View):
        def post(self,request):
            data = json.loads(request.body)





       

   


