import json
import re
import bcrypt
import jwt
import os
import sys
sys.path.append(os.path.dirname('/Users/mac/Desktop/wecode_dev/21-Westagram-backend/students/sanghyub/21-Westagram-backend/students/sanghyub'))
import datetime

from django.db.models.fields import EmailField
from django.views import View
from django.http  import JsonResponse, HttpResponse 
from django.core  import exceptions, validators

from user.models    import User
from .models        import Posting, Image
from sanghyub.utils   import jwt_token_decorator



class UserPost(View):
    @jwt_token_decorator
    def post (self,request): 
        try:
            data = json.loads(request.body)
           
            Posting.objects.create(
                user_id = request.user.id,
                context = data["context"]
            )
            
            # Image.objects.create(
            #     post_id = Posting.objects.get()
            #     image = data["image"]
            # )

            return JsonResponse({"message":"Created!"}, status = 200)
        except KeyError:
            return JsonResponse({"message": "INVALID KEY"}, status = 400)

    # @jwt_token_decorator
    # def get (self,request):
    #     try:
    #         posting = Posting.objects

    #         post_info = {
    #             "user" : User.objects
    #         }

            
        
    #         return JsonResponse({"message":"Created!"}, status = 200)
    #     except KeyError:
    #         return JsonResponse({"message": "INVALID KEY"}, status = 400)

    



