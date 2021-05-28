from django.views import View
from django.http import JsonResponse

class UserView(View):
    def post(self, request):
        return JsonResponse({'massage': 'SUCCESS'}, status=200)