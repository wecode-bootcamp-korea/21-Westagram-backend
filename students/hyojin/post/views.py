import json

from django.views import View
from django.http  import JsonResponse

from .models     import Post, Image
from user.models import User

class PostUploadView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            token = request.META.get('HTTP_AUTHORIZATION')
            
            user = User.objects.get(email=data['email'])

            content     = data.get('content')
            image_urls  = data.get('url')

            post = Post(
                user    = user,
                content = content,
            )

            post.save()

            if image_urls != None:
                for url in image_urls:
                    image_object = Image(post = post, url = url)
                    image_object.save()

            return JsonResponse({'message':'SUCCESS'}, status=201)
            
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=200)

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
