import json
from json.decoder                 import JSONDecodeError

from django.views                 import View
from django.http.response         import JsonResponse
from django.db.models.expressions import F

from users.models                 import post
from .models                      import Posting

class PosingView(View):
    def post(self, request):
        try:
            data = json.loads(request)
            user = User.Objects.get(email=data['email'])

            Posting.objects.create(
                user      = user,
                title     = data['title'],
                main_text = data['main_text']
                )

            JsonResponse({'message': 'CREATED'}, status=201)

        except ValueError:
            return JsonResponse({'message': 'INVALIED_DATA'}, status=400)

        except JSONDecodeError:
            return JsonResponse({'message': 'NO_BODY_DATA'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message': 'NO_EXIST_USER'}, status=409)

        def get(self, request):
            result = [
                posting for posting in Posting.objects.all().values(
                'title', 'main_text', 'created_at', user=F('user__email')
                )]
                
            JsonResponse({'message': result}, status=200)