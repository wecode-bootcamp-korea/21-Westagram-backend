from django.views import View
from django.http import JsonResponse
from .models import User
import json


class UserView(View):
    def post(self, request):
        data = json.loads(request.body)
        User.objects.create(
        user_name    = data['user_name'],
        phone_number = data['phone_number'],
        user_email   = data['user_email'],
        passward     = data['passward']
        )
        return JsonResponse({'massage': 'SUCCES'}, status = 201)



