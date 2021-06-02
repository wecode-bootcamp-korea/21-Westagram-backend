import json, jwt
from json.decoder            import JSONDecodeError

from django.views            import View
from django.http.response    import JsonResponse
from django.db               import transaction
from django.db.utils         import DataError

from users.models            import User
from .models                 import Posting, PostingImage
from westagram.settings      import SECRET_KEY, HASH_ALGORITHM

class PostingView(View):
    def post(self, request):
        try:
            data       = json.loads(request.body)
            token      = request.headers['token']
            image_urls = data['image_urls']
            user_id    = jwt.decode(token, SECRET_KEY, 
                                    algorithms=HASH_ALGORITHM)['user_id']

            if type(image_urls) is not list:
                return JsonResponse({'message': 'INVALIED_DATA'}, status=400)

            with transaction.atomic():
                new_posting = Posting.objects.create(
                    user      = User.objects.get(id=user_id),
                    main_text = data['main_text']
                    )

                for image_url in image_urls:
                    PostingImage.objects.create(
                        posting = new_posting,
                        url     = image_url
                        )

            return JsonResponse({'message': 'CREATED'}, status=201)

        except KeyError:
            return JsonResponse({'message': 'INVALIED_DATA'}, status=400)

        except JSONDecodeError:
            return JsonResponse({'message': 'NO_BODY_DATA'}, status=400)

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message': 'INVALIED_TOKEN'}, status=401)
        
        except DataError:
            return JsonResponse({'message': 'INVALIED_DATA'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message': 'NO_EXIST_USER'}, status=401)

        except User.MultipleObjectsReturned:
            return JsonResponse({'message': 'NO_EXIST_USER'}, status=401)

    def get(self, request):
        result   = [self.make_posting_response_data(posting) 
                    for posting in Posting.objects.all()]

        return JsonResponse({'message': result}, status=200)
    
    def get(self, request, id):
        try:
            posting = Posting.objects.get(id=id)
            result = self.make_posting_response_data(posting)
            
            return JsonResponse({'message': result}, status=200)

        except Posting.DoesNotExist:
            return JsonResponse({'message': 'NOT_FOUND'}, status=404)

        except Posting.MultipleObjectsReturned:
            return JsonResponse({'message': 'NOT_FOUND'}, status=404)

    def make_posting_response_data(self, posting):
        return {
                'user'       : posting.user.email,
                'main_text'  : posting.main_text,
                'created_at' : posting.created_at
                                .strftime('%Y-%m-%d %H:%M:%S %z %Z'),
                'image_urls' : list(
                    posting.postingimage_set.all()
                    .values_list('url', flat=True))
                }