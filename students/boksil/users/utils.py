import jwt

from django.http import JsonResponse

from users.models       import User
from westagram.settings import SECRET_KEY, ALGORITHM

def trace(func):
    def wrapper(self, request):        

        if "Authorization" not in request.headers:
            return JsonResponse({'message': 'INVALID_LOGIN'}, status=401)
        
        encode_token = request.headers["Authorization"]

        try:
            data = jwt.decode(encode_token, SECRET_KEY, ALGORITHM)

            user = User.objects.get(id = data["id"])
            request.user = user

        except jwt.DecodeError:
            return JsonResponse({"message": "INVALID_TOKEN"}, status=401)
        
        except User.DoesNotExist:
            return JsonResponse({"message": "UNKNOWN_USER"}, status=401)
        
        return func(self, request, *args, **kwargs)

    return wrapper

