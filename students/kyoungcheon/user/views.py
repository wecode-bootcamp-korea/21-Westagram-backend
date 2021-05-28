import json

from django.views import View
from django.http  import JsonResponse

from .models import Member

class Sign(View):
    def post(self, request):
        # try:
        #     data = json.loads(request.body)
        return JsonResponse({'message': "gogo"},status=200)