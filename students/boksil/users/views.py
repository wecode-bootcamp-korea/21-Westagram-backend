import json, re

from django.views import View
from django.http  import JsonResponse

from .models import User

email_regex = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

class SignupView(View):
    def post(self, request):
        
        try:
            # data 변수를 생성하여 요청받은 정보를 json으로 변환 후 담아둔다.
            data = json.loads(request.body)

            email = data['email']

            # unique=True가 안 먹혀서 중복 조건식 지정 (완료)
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'massage': 'KEY_ERROR_EMAIL_EXIST)'}, status=400)

            elif User.objects.filter(mobile=data['mobile']).exists():
                return JsonResponse({'massage': 'KEY_ERROR_MOBILE_EXIST)'}, status=400)

            elif User.objects.filter(nickname=data['nickname']).exists():
                return JsonResponse({'massage': 'KEY_ERROR_NICKNAME_EXIST)'}, status=400)

            # 이메일 정규식 사용 (email validation)
            elif not email_regex.match(email):
                return JsonResponse({'message':'PLEASE ENTER @ or .'}, status=400)

            # password가 8자리 미만인 경우 에러 발생 (완료)
            elif len(data['password']) < 8:
                return JsonResponse({'massage': 'KEY_ERROR_PASSWORD'}, status=400)

            # 위 조건식이 모두 아닌 경우 아래의 데이터 생성
            else:
                User.objects.create(
                    email    = data['email'],
                    password = data['password'],
                    mobile   = data['mobile'],
                    nickname = data['nickname']
                    )
            
            # else 조건 만족 시 리턴
            return JsonResponse({'massage': 'SUCCESS'}, status=201)
        
        except KeyError:
            return JsonResponse({'massage': 'KEY_ERROR'}, status=400)
