import json
import re

from django.views import View
from django.http  import JsonResponse

from .models import User

class UserView(View):
    def reg_validation(self, user_datas):
        email    = user_datas['email'] if user_datas.get('email') else ''
        password = user_datas['password'] if user_datas.get('password') else ''
        phone_no = user_datas['phone_no'] if user_datas.get('phone_no') else ''
        full_nm  = user_datas['full_nm'] if user_datas.get('full_nm') else ''
        user_nm  = user_datas['user_nm'] if user_datas.get('user_nm') else ''

        if (email == '' or 
            not re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$').match(email)):
            return [False, 'KEY_ERROR', 'EMAIL']
        elif password == '' or len(password) < 8:
            return [False, 'KEY_ERROR', 'PASSWORD']
        elif phone_no == '' or re.compile('').match() == None:
            return [False, 'KEY_ERROR', 'PHONE_NO']
        elif full_nm == '':
            return [False, 'KEY_ERROR', 'FULL_NM']
        elif user_nm == '':
            return [False, 'KEY_ERROR', 'USER_NM']

        if len(User.objects.filter(email=email)) > 0:
            return [False, 'VALUE_DUP', 'EMAIL']

        if len(User.objects.filter(phone_no=phone_no)) > 0:
            return [False, 'VALUE_DUP', 'PHONE_NO']

        if len(User.objects.filter(user_nm=user_nm)) > 0:
            return [False, 'VALUE_DUP', 'USER_NM']

        return [True, '', '']

    # 연동테스트
    # def get(self, request):
    #     print('hello')
    #     return JsonResponse({'result':'SUCCESS'}, status=200)

    def post(self, request):
        try:
            user_datas = json.loads(request.body)
            valid_list = self.reg_validation(user_datas)

            if not valid_list[0]:
                return JsonResponse({
                    'result': f'{valid_list[1]}_{valid_list[2]}'
                }, status=400)
            
            User.objects.create(
                email=user_datas['email'],
                password=user_datas['password'],
                phone_no=user_datas['phone_no'],
                full_nm=user_datas['full_nm'],
                user_nm=user_datas['user_nm']
            )

            return JsonResponse({'result':'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'result':'INVALID_KEY'}, status=400)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'result':'INVALID_REQUEST_BODY'}, status=400)
