import json

from django.views     import View
from django.http      import JsonResponse

from board.models     import Board, Image
from user.models      import User

class PostView(View):
    def post(self,request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(email=data['email']).exists():
                user = data['email'] 
            title = data['title']
            picture = data['picture']
            
            Board.objects.create(
            user = user,
            title = title,
            picture= picture
            )
          
        except KeyError: 
            return JsonResponse({'message':'KEY_ERROR'}, status=400) 
        except User.DoesNotExist:
            return JsonResponse ({'message':'USER_DOSE_NOT_EXIST'}, status=400)  
            

