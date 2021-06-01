import json
from django.core.exceptions import ValidationError

from django.http  import JsonResponse
from django.views import View
from .models      import User
from .validators  import validate_phone, validate_email, validate_password, validate_nickname

class UserView(View):
    def post(self,request):
        try:
            data = json.loads(request.body)
        
            email_data        = data['email'] 
            password_data     = data['password'] 
            nickname_data     = data['nickname'] 
            phone_number_data = data['phone_number'] 

            validate_email(email_data)
            validate_password(password_data)
            validate_phone(phone_number_data)
            validate_nickname(nickname_data)

            User.objects.create(
                email        = email_data,
                password     = password_data,
                nickname     = nickname_data,
                phone_number = phone_number_data)

            return JsonResponse({'result':'SUCCESS'}, status=201)
        
        except KeyError:
            return JsonResponse({'message':'INVALID_KEY'}, status=400)
        except ValidationError as e:
            return JsonResponse({'message':str(e)}, status=400)
