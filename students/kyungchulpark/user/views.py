import json

from django.http  import JsonResponse
from django.views import View
from .models      import User
from .validators  import validate_phone,validate_email,validate_password,validate_nicname

class UserView(View):
    def post(self,request):
        try:
            data = json.loads(request.body)
        
            email_data    = data['email'] 
            password_data = data['password'] 
            nicname_data  = data['nicname'] 
            phone_data    = data['phone'] 

            validate_email(email_data)
            validate_password(password_data)
            validate_phone(phone_data)
            validate_nicname(nicname_data)

            User.objects.create(
                email=email_data,
                password=password_data,
                nicname=nicname_data,
                phone=phone_data)

            return JsonResponse({'result':'SUCCESS'}, status=201)
        
        except KeyError:
            return JsonResponse({'message':'INVALID_KEY'}, status=400)
        except Exception as e:
            return JsonResponse({'message':str(e)}, status=400)
