import jwt
import json
from django.views   import View
from django.http    import JsonResponse

from .models        import Postboard
from userapp.models import User
from my_settings    import SECRET_KEY,ALGORITHM



class PostView(View):
    def post(self,request):
         try:
            data  = json.loads(request.body)
            token = request.headers['token']
            aut = jwt.decode(token,SECRET_KEY,ALGORITHM)
         
            if not User.objects.filter(email=aut['email']).exists():
                return JsonResponse({'이메일형식 및 닉네임 정보가 맞지 않습니다.'},status=400)
            user = User.objects.get(email=aut['email'])
            Postboard.objects.create(
                user         = user,
                contensboard = data['contens'],
                img_url      = data['imgurl'])
            return JsonResponse({'MESSAGE':'성공적으로 끝났습니다.'},status=201)

           
         except KeyError:
            return JsonResponse({'message':'키에러'},status=400)
        
