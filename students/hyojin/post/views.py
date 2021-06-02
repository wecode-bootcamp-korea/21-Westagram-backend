import json
import jwt

from django.views import View
from django.http  import JsonResponse
from django.core.exceptions import MultipleObjectsReturned

from .models     import Post, Image
from user.models import User
from my_settings import ALGORITHM, SECRET_KEY

def decorator(func):
    def wrapper(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
            user  = jwt.decode(token, SECRET_KEY, ALGORITHM)

            user_object = User.objects.get(id=user['user_id'])

            return func(self, request, user_object)

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message':'INVALID_TOKEN_TYPE'}, status=400)   

        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=401)

    return wrapper

class PostUploadView(View):
    @decorator
    def post(self, request, user):
        try:
            data = json.loads(request.body)

            content     = data.get('content')
            image_urls  = data.get('image_urls')

            post = Post(
                user    = user,
                content = content
            )

            post.save()
    
            if image_urls != None:
                for url in image_urls:
                    image_object = Image(post = post, url = url)
                    image_object.save()
            
            return JsonResponse({'message':'SUCCESS'}, status=201)
            
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=200)
        
        except MultipleObjectsReturned:
            return JsonResponse({'message':"MULTIPLE_KEY_RETURN"}, status=500)

class AllPostView(View):
    def get(self, request):
        posts = Post.objects.all()

        post_list = [] 

        for post in posts:
            post_object = {
                'user'         : post.user.id,
                'content'      : post.content,
                'created_time' : post.created_time
            }
            post_list.append(post_object)
        
        return JsonResponse({'message':{'post':post_list}}, status=200)
