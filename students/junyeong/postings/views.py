import json

from django.views import View
from django.http  import JsonResponse

from .models import Posting

from user.models import User

class PostingView(View):
    
    def post(self, request):

        try:
            data = json.loads(request.body)
            print(User.email)
            user = User.objects.get(email = data['email'])

            Posting.objects.create(
            img_url  = data['img_url'],
            user     = user
            )

            if not User.objects.filter(email = data['email']).exists():
                return JsonResponse({'message': 'INVALID_USER'}, status= 401)

            return JsonResponse({'message': 'SUCCESS'}, status= 201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status= 400)

class Post_updateView(View):

    def get(self, request):
        
        posting_data = Posting.objects.values()
        return JsonResponse({'posting_data': list(posting_data)}, status = 200)


    

