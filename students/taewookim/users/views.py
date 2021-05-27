from django.views         import View
from django.http.response import JsonResponse

from .models              import User

class UserView(View):
    def post(self, request):
        return JsonResponse({"result": "CREATED"}, status=201)