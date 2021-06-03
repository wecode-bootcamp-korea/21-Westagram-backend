import json, jwt

from django.views import View
from django.http  import JsonResponse

from .models import Posting
from user.models import User
from my_settings import SECRET_KEY, ALGORITHM
from django.db.models  import F

class PostingView(View):
    
    def post(self, request):

        try:
            data = json.loads(request.body)
            token      = request.headers['token']
            
            Posting.objects.create(
            img_url  = data['img_url'],
            user     = jwt.encode(token, SECRET_KEY, algorithm=ALGORITHM)
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
        


    

