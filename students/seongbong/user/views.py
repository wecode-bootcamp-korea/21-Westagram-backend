import json, re, bcrypt, jwt


from django.core.exceptions import ObjectDoesNotExist
from westagram.settings     import SECRET_KEY, ALGORITHM
from django.http            import JsonResponse
from django.db              import IntegrityError
from django.views           import View 
from .models                import User 

class UserSignUp(View):
    def post(self, request):

        email_regex       = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        data              = json.loads(request.body)
        signup_data       = User.objects
        hashed_pw         = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        decoded_hashed_pw = hashed_pw.decode('utf-8')
        
        try:
            if not re.match(email_regex, data['email']):
                return JsonResponse({'message': 'EMAIL_ERROR'}, status=400) 
            
            if len(data['password']) < 8:
                return JsonResponse({'message': 'PASSWORD_ERROR'}, status=400)
            
            if signup_data.filter(nickname = data['nickname']).exists(): 
                return JsonResponse({'message': 'UNIQUE_ERROR'}, status=400)

            if signup_data.filter(phone_number = data['phone_number']).exists():
                return JsonResponse({'message': 'UNIQUE_ERROR'}, status=400)    

            User.objects.create(
                email        = data['email'],
                password     = decoded_hashed_pw,
                nickname     = data['nickname'],
                phone_number = data['phone_number']
            )
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except IntegrityError:
            return JsonResponse({'message': 'UNIQUE_ERROR'}, status=400)
        
        return JsonResponse({'message': 'SUCCESS'}, status=201)
        
class UserSignin(View):
    def post(self, request):
        try:
            data            = json.loads(request.body)
            email           = data['email']
            password        = data['password'].encode('utf-8')

            if email == "" or password == "":
                return JsonResponse({"message": "KEY_ERROR"}, status=400)

            signin_user  = User.objects.get(email=email)
            encoded_db_password  = signin_user.password.encode('utf-8')

            if not bcrypt.checkpw(password, encoded_db_password):
                return JsonResponse({"message": "INVALID_USER"}, status=401)

            user       = {"user_id" : signin_user.id}
            encode_jwt = jwt.encode(user, SECRET_KEY, ALGORITHM)
            return JsonResponse({"token" : encode_jwt, "message" : "SUCCESE"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status=401)
        