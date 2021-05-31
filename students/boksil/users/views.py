import json

from django.views import View
from django.http  import JsonResponse

from .models import User

class SignupView(View):
    def post(self, request):
        
        try:
            # data 변수를 생성하여 요청받은 정보를 json으로 변환 후 담아둔다.
            data = json.loads(request.body)

            email = data['email']

            # unique=True가 안 먹혀서 중복 조건식 지정 (완료)
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'massage': 'KEY_ERROR(email_exists)'}, status=400)

            elif User.objects.filter(mobile=data['mobile']).exists():
                return JsonResponse({'massage': 'KEY_ERROR(mobile_exists)'}, status=400)

            elif User.objects.filter(nickname=data['nickname']).exists():
                return JsonResponse({'massage': 'KEY_ERROR(nickname_exists)'}, status=400)

            # email에 @, . 이 없는 경우 에러 발생 (완료)
            # (질문) '@' or '.' not in email: @ 또는 . 이 없는경우 
            # 에러 발생하란 조건을 줬지만 @와 .이 다 있는 상황에도 에러가 발생하였음
            elif '@' not in email or '.' not in email:
                return JsonResponse({'message':'PLEASE ENTER @ or .'}, status=400)

            # password가 8자리 미만인 경우 에러 발생 (완료)
            elif len(data['password']) < 8:
                return JsonResponse({'massage': 'KEY_ERROR(password)'}, status=400)

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
            return JsonResponse({'massage': 'KEY_ERROR(key)'}, status=400)
