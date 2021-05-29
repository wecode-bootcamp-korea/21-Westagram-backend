#from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views import View
#from user.models import Join


# Create your views here.
'''
class JoinView(View):
    def get(self, request):

        try:
            data = json.loads(request.body)
            if 'email' in data.keys():









        except KeyError:
            return JsonResponse({'message':'INVALID_USER'}, status=400)
'''