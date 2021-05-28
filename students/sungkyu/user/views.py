import json, re

from django.views import View
from django.http  import JsonResponse

from .models      import Users

class SignupView(View):
    def post(self, request):

        user_email           = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        user_phonenumber     = '^[0-9]{3}-[0-9]{4}-[0-9]{4}$'
        user_password        = '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,18}$'

        data                 = json.loads(request.body)
        email_savedata       = Users.objects.filter(email = data['email'])
        phonenumber_savedata = Users.objects.filter(phonenumber = data['phonenumber'])
        nickname_savedata    = Users.objects.filter(nickname = data['nickname'])
        
        # email과 password의 값이 들어있지 않은 경우
        # email과 password의 KEY값이 일치하지 않을 경우 keyerror 리턴
        try:
            if '' == data['email']:
                return JsonResponse({'message': 'INVALID_EMAI'}, status=400)

            elif '' == data['password']:
                return JsonResponse({'message': 'INVALID_PASSWORD'}, status=400)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        # email과 password, phonenumber가 정규표현식에 부합하지 않는 경우
        if not re.match(user_email, data['email']):
            return JsonResponse({'message': 'INVALID_EMAIL'}, status=400)

        elif not re.match(user_phonenumber, data['phonenumber']):
            return JsonResponse({'message': 'INVALID_PHONENUMBER'}, status=400)

        elif re.match(user_password, data['password']):
            return JsonResponse({'message': 'INVALID_PASSWORD'}, status=400)

        # 중복검사
        if   email_savedata.count() == 1:
            return JsonResponse({'MESSAGE' : 'EMAIL_OVERLAP_ERROR'}, status=400)

        elif phonenumber_savedata.count() == 1:
            return JsonResponse({'MESSAGE' : 'POHNENUMBER_OVERLAP_ERROR'}, status=400)

        elif nickname_savedata.count() == 1:
            return JsonResponse({'MESSAGE' : 'NICKNAME_OVERLAP_ERROR'}, status=400)

        Users.objects.create(
            email       = data['email'],
            password    = data['password'],
            phonenumber = data['phonenumber'],
            nickname    = data['nickname'],
        )

        return JsonResponse({'message': 'SUCCESS'}, status=201)

    def get(self, request):
        return JsonResponse({'message': 'SUCCESS'}, status=200)

