import json

from django.views import View
from django.http  import JsonResponse
from django.db    import IntegrityError
from .models      import User


class NewUserView(View) :

    def post(self, request) :

        try:
            data = json.loads(request.body)

            User.objects.create(

                nickname   = data['nickname'],
                email      = data['email'],
                password   = data['password'],
                phonenumber= data['phonenumber']

                )
            return JsonResponse({'message':'SUCCESS'}, status=201)

        except KeyError :
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except IntegrityError : # 중복예외처리
            return JsonResponse({"message": "INTERGRITY_ERROR"}, status=400)

        


