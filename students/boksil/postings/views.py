import json

from django.views import View
from django.http  import JsonResponse

from users.utils  import Trace
from users.models import User
from .models      import Posting

class PostUploadView(View):
        def post(self, request):
            data = json .loads(request.body)

            try:

                return JsonResponse({'message': 'SUCCESS'}, status=200)

            except KeyError:
                return JsonResponse({'message': 'KEY_ERROR'}, status=400)