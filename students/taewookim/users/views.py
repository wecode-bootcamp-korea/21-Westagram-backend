import json, re, bcrypt, jwt
from json.decoder            import JSONDecodeError

from django.views            import View
from django.http.response    import JsonResponse
from django.db.models        import Q, F

from .models                 import User, FollowingFollower
from westagram.settings      import SECRET_KEY, HASH_ALGORITHM

EMAIL_REGEX    = '^([a-z0-9_+.-]+@([a-z0-9-]+\.)+[a-z0-9]{2,4}){1,50}$'
PASSWORD_REGEX = '^.{8,30}$'
NICKNAME_REGEX = '^.{2,10}$'
PHONE_REGEX    = '^01[016789]\-\d{3,4}\-\d{4}$'

class UserView(View):
    def post(self, request):
        try:
            data         = json.loads(request.body)
            email        = data['email']
            password     = data['password']
            nickname     = data['nickname'] 
            phone_number = data['phone_number']

            if not re.match(EMAIL_REGEX, email):
                return JsonResponse({"message": "INVALIED_EMAIL"}, status=400)

            if not re.match(PASSWORD_REGEX, password):
                return JsonResponse({"message": "INVALIED_PASSWORD"}, status=400)

            if not re.match(NICKNAME_REGEX, nickname):
                return JsonResponse({"message": "INVALIED_NICKNAME"}, status=400)

            if not re.match(PHONE_REGEX, phone_number):
                return JsonResponse({"message": "INVALIED_PHONE_NUMBER"}, status=400)

            if User.objects.filter(
                Q(email=email) | 
                Q(nickname=nickname) | 
                Q(phone_number=phone_number)).exists() :
                return JsonResponse({"message": "DUPLICATED_INFORMATION"}, status=409)

            User.objects.create(
                email        = email,
                password     = bcrypt.hashpw(password.encode('utf-8'),
                                             bcrypt.gensalt()).decode('utf-8'),
                phone_number = phone_number,
                nickname     = nickname
            )

            return JsonResponse({"message": "CREATED"}, status=201)

        except JSONDecodeError:
            return JsonResponse({"message": "EMPTY_BODY_DATA"}, status=400)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)




class LoginView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']
            user     = User.objects.get(email=email)

            if not bcrypt.checkpw(password.encode('utf-8'),
                                  user.password.encode('utf-8')):
                return JsonResponse({"message": "INVALID_USER"}, status=401)

            return JsonResponse({
                                 "message": "SUCCESS",
                                 "token"  : jwt.encode({'user_id': user.id}, 
                                                SECRET_KEY, 
                                                algorithm=HASH_ALGORITHM)
                                }, status=200)

        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status=401)
        
        except User.MultipleObjectsReturned:
            return JsonResponse({"message": "INVALID_USER"}, status=401)    
        
        except JSONDecodeError:
            return JsonResponse({"message": "EMPTY_BODY_DATA"}, status=400)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

def follow_user(request, following_user_id):
    if request.method == 'POST':
        try:
            token   = request.headers['token']
            follower_user_id  = jwt.decode(token, SECRET_KEY, 
                                    algorithms=HASH_ALGORITHM)['user_id']

            follower_user     = User.objects.get(id=follower_user_id)
            following_user    = User.objects.get(id=following_user_id)

            if follower_user == following_user:
                return JsonResponse({
                        "message": "CAN_NOT_FOLLOW_YOURSELF"}, status=403)
            
            if FollowingFollower.objects.filter(following_user=following_user,
                                    follower_user=follower_user).exists():  
                return JsonResponse({
                        "message": "ALREADY_FOLLOWED_USER"}, status=409)

            FollowingFollower.objects.create(following_user=following_user,
                                follower_user=follower_user)

            return JsonResponse({"message": "SUCCESS"}, status=200)

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message': 'INVALIED_TOKEN'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status=401)
        
        except User.MultipleObjectsReturned:
            return JsonResponse({"message": "INVALID_USER"}, status=401)    

        except KeyError:
            return JsonResponse({"result": "KEY_ERROR"}, status=400)
    
    else:
        return JsonResponse({"message": "METHOD_NOT_ALLOWED"}, status=405)

def unfollow_user(request, following_user_id):
    if request.method == 'POST':
        try:
            token   = request.headers['token']
            follower_user_id  = jwt.decode(token, SECRET_KEY,
                                    algorithms=HASH_ALGORITHM)['user_id']
            follower_user     = User.objects.get(id=follower_user_id)
            following_user    = User.objects.get(id=following_user_id)

            if follower_user == following_user:
                return JsonResponse({
                        "message": "CAN_NOT_UNFOLLOW_YOURSELF"}, status=403)

            FollowingFollower.objects.get(
                            following_user=following_user, 
                            follower_user=follower_user).delete()

            return JsonResponse({"message": "SUCCESS"}, status=200)

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message': 'INVALIED_TOKEN'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status=401)
        
        except User.MultipleObjectsReturned:
            return JsonResponse({"message": "INVALID_USER"}, status=401)

        except FollowingFollower.DoesNotExist:
            return JsonResponse({"message": "NO_FOLLOWED_THIS_USER"}, status=403)
        
        except FollowingFollower.MultipleObjectsReturned:
            return JsonResponse({"message": "INVALID_USER"}, status=401)    

        except KeyError:
            return JsonResponse({"result": "KEY_ERROR"}, status=400)

    else:
        return JsonResponse({"message": "METHOD_NOT_ALLOWED"}, status=405)

def get_follower(request, user_id):
    if request.method == 'GET':
        try:
            user = User.objects.get(id=user_id)
            followers = list(FollowingFollower.objects
                                               .filter(following_user=user)
                                               .select_related('user')
                                               .values_list('follower_user__email',
                                               flat=True))
            
            
            return JsonResponse({'message': followers}, status=200)   

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message': 'INVALIED_TOKEN'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status=401)

    else:
        return JsonResponse({"message": "METHOD_NOT_ALLOWED"}, status=405)

def get_following(request, user_id):
    if request.method == 'GET':
        try:
            user = User.objects.get(id=user_id)
            followings = list(FollowingFollower.objects
                                                .filter(follower_user=user)
                                                .select_related('user')
                                                .values_list('following_user__email',
                                                flat=True))
            
            return JsonResponse({'message': followings}, status=200)   

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message': 'INVALIED_TOKEN'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status=401)

    else:
        return JsonResponse({"message": "METHOD_NOT_ALLOWED"}, status=405)