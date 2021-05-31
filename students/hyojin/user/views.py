import json
from django.db.models.fields import IntegerField

from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import ValidationError
from django.db              import IntegrityError

from .models import User

class NewUserView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            user = User(
                email        = data['email'], 
                password     = data['password'], 
                phone_number = data.get('phone_number'), 
                nickname     = data.get('nickname')
            )

            user.phone_number = user.check_blank(user.phone_number)
            user.nickname     = user.check_blank(user.nickname)
            
            user.full_clean()
            user.save()

            return JsonResponse({'message':'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        except IntegrityError:
            return JsonResponse({"message":"이미 존재하는 값 입니다."}, status=400)

        except ValidationError as e: 
            return JsonResponse({'message':e.message_dict}, status=400)

       