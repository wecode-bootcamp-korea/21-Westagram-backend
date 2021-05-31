import json
from json.decoder                 import JSONDecodeError

from django.views                 import View
from django.http.response         import JsonResponse
from django.db                    import transaction
from django.db.models.expressions import F

from users.models                 import User
from .models                      import Posting, PostingImage

class PosingView(View):
    def post(self, request):
        try:
            data = json.loads(request)

            with transaction.atomic():
                new_posting = Posting.objects.create(
                    user      = User.Objects.get(email=data['email']),
                    main_text = data['main_text']
                    )

                for image_url in data['image_urls']:
                    PostingImage.objects.create(
                        posting = new_posting,
                        url     = image_url
                        )

            JsonResponse({'message': 'CREATED'}, status=201)

        except ValueError:
            return JsonResponse({'message': 'INVALIED_DATA'}, status=400)

        except JSONDecodeError:
            return JsonResponse({'message': 'NO_BODY_DATA'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message': 'NO_EXIST_USER'}, status=409)

    def get(self, request):
        postings = Posting.objects.all()
        result   = []

        for posting in postings:
            result.append({
                'user'       : posting.user.email,
                'main_text'  : posting.main_text,
                'created_at' : posting.created_at,
                'image_urls' : list(
                    posting.postingimage_set.all()
                    .values_list('url', flat=True))
                })
            
        JsonResponse({'message': result}, status=200)