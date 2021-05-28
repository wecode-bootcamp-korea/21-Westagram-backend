import json
from json.encoder import JSONEncoder
from django.views import View
from django.http  import JsonResponse
from .models      import Signup

class SignupListView(View):

    def post(self, request):
        data = json.loads(request.body)

        try:
            Signup.objects.create(
            name     = data['name'],
            email    = data['email'],
            password = data['password'],
            number   = data['number']
            )
            
            return JsonResponse({'message': 'SUCCESS'}, status= 201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status= 400)