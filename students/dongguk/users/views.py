import json, re, bcrypt, jwt    #파이썬 내장모듈  Django랑 상관없음 즉, 항상 쓸 수 있다.

from westagram.settings import DEFAULT_AUTO_FIELD

from django.views       import View
from django.http        import JsonResponse

from .models            import User  #어디다가 create 할 건지 알아야 하기 때문에 그 정보는 여기에 있다 라는걸 표시 해야한다.
from my_settings        import SECRET_KEY, ALGORITHM  # 6/2 로그인시 필요한 데이터여서 불러와야함

re_password = "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$" #비밀번호 8~18 설정 및 정규식표현

class SignupView(View):
    def post(self, request):
        
        try:
            data = json.loads(request.body) #파이썬언어로 변화하고, data변수로 저장한다.
            nickname     = data['nickname']
            password     = data['password']
            phone_number = data['phone_number']
            email        = data['email']
           
            # 닉네임이 존재할 경우
            #.exists: 이 메서드는 최소한 하나의 레코드가 존재하는지 여부를 확인하여 알려주는 메서드이다.
            #.filter: 데이터를 다 가져온다는 뜻이다.
            # status=400 : 잘못된 요청, 요청구문이 잘못됨                                                    
            if User.objects.filter(nickname = data['nickname']).exists():                                                   
                return JsonResponse({'message': 'INVALID_NICKNAME'}, status=400)
            # 전화번호가 존재할 경우 
            if  User.objects.filter(phone_number = data['phone_number']).exists():
                return JsonResponse({'message': 'INVALID_PHONE_NUMBER'}, status=400)
            # 이메일이 존재할 경우
            if User.objects.filter(email = data['email']).exists():
                return JsonResponse({'message': 'INVALID_EMAIL'}, status=400)
            #@,. 이 포함되지 않은 경우
            if '@' not in email or '.' not in email:
                return JsonResponse({'message': 'INVALID_EMAIL'}, status=400)
            # 정규식
            if not re.match(re_password, data['password']):
                return JsonResponse({'message': 'INVALID_PASSWORD'}, status=400)
            # 6/2 비밀번호 암호화 코드 >> 해싱(인코딩 변환).(디코딩 변환) 데이터 형식맞출라고 코드를 씀
            bcr_password= bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8') 
            #위에 조건이 맞는경우
            User.objects.create(
                nickname     = nickname,
                password     = bcr_password,   # 6/2 기존 password에서 암호화 시킨 bcr_password 값으로 바꿈 
                phone_number = phone_number,
                email        = email
                
            )
            #정상적으로 작동하면 나타나지는 코드                                                                
            return JsonResponse({'message': 'SUCCESS'}, status=201)
        #에러가 나는경우
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        
class LoginView(View):
    def post(self, request):
        
        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']
            
            if not User.objects.filter(email = email).exists():
                return JsonResponse({'message': 'INVALID_USER'}, status=401)

            user = User.objects.get(email=email)
             # 6/2 비밀번호 암호화 코드가 맞는지 안맞는지 체크
            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                  return JsonResponse({'message': 'INVALID_USER'}, status=401)
             # 6/2 로그인 성공시 토크값을 주는 코드     
            return JsonResponse({'message': 'SUCCESS', 'user_token' : jwt.encode({'id': user.id}, SECRET_KEY, ALGORITHM)}, status=200)       
        except KeyError:
           return JsonResponse({'message': 'KEY_ERROR'}, status=400)
                