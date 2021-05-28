import json
import re

from django.views    import View
from django.http     import JsonResponse
from django.db.utils import IntegrityError

from .models import Member

email_regex = "^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

class Sign(View):
    def post(self, request):
        try:
            data          = json.loads(request.body)
            email_data    = data['email']
            password_data = data['password']
            phone_data    = data.get('phone')
            nickname_data = data.get('nickname')

            if len(password_data) < 8:
                return JsonResponse({'message': '비밀번호 8자이상 작성해주세요.'}, status=400)
            if not(re.search(email_regex, email_data)):
                return JsonResponse({'message': '이메일 형식에 맞게 작성해주세요.'}, status=400)

            Member.objects.create(
                            email    = email_data,
                            password = password_data,
                            phone    = phone_data,
                            nickname = nickname_data
                            )

            return JsonResponse({'message': "SUCCESS"}, status=201)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        except IntegrityError as e:
            if email_data in str(e):
                return JsonResponse({'message':"이메일 중복입니다."}, status=400)
            if phone_data in str(e):
                return JsonResponse({'message':"핸드폰번호 중복입니다."}, status=400)
            if nickname_data in str(e):
                return JsonResponse({'message':"닉네임 중복입니다."}, status=400)
