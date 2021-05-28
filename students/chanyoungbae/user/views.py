import json
import re

from django.views import View
from django.http import JsonResponse
from .models import User

class SignUpView(View):
    def post(self, request):
        try:
            data      = json.loads(request.body)

            email     = data['email']
            password  = data['password']
            phone_num = data['phone_num']
            name      = data['name']

            email_regex    = '^([\w\.\-_]+)?\w+@[\w]+(\.\w+){1,}$'
            password_regex = '^([a-zA-Z0-9~!@#$%^&*()_+]).{7,}$'

            

            if not email or not password:
                return JsonResponse({"message": "KEY_ERROR"}, status = 400)

            if re.match(email_regex , email) == None :
                return JsonResponse({"message": "INVALID_VALUE"}, status = 400)

            if re.match(password_regex, password) == None:
                return JsonResponse({"message": "SHORT PASSWORD"}, status =400)
            
            User.objects.create(
                name      = name, 
                email     = email,
                phone_num = phone_num,
                password  = password
            )

            return JsonResponse({"result":"SUCCESS"}, status = 201)
            
        except KeyError:
            return JsonResponse({"message": "KEY_ERRORs"}, status = 400)