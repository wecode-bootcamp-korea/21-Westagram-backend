import json
import re
import bcrypt
import jwt

from django.views      import View
from django.http       import JsonResponse
from django.db.models  import Q
from django.db         import IntegrityError

from mysettings        import SECRET_KEY, ALGORYTHM
from .models           import User

class UserSignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            account_regex      = re.compile('^[A-Za-z0-9\.+_-]+\@[A-Za-z0-9\._-]+\.[a-zA-Z]+$')
            phone_number_regex = re.compile('^[0-9]{3}\-*[0-9]{3,4}\-*[0-9]{3,4}$')
            
            #uniqueness check(account,phone_number,nickname)
            if User.objects.filter(
                Q(account      =data['account'])|
                Q(phone_number =data['phone_number'])|
                Q(nickname     =data.get('nickname'))).exists():
                return JsonResponse({'message': 'ACCOUNT or PHONE NUMBER or NICK NAME ALEADY EXISTS'}, status=400)

            # account validation
            if not account_regex.match(data['account']):
                return JsonResponse({'message':'INPUT ERROR'}, status=400)

            # password validation
            if len(data['password']) < 8:
                return JsonResponse({'message': 'INPUT ERROR'}, status=400)
            
            # password encrypt
            password_encoded = data['password'].encode('utf-8')
            salt = bcrypt.gensalt()
            password_hashed = bcrypt.hashpw(password_encoded, salt)
            password_decoded = password_hashed.decode('utf-8')

            # phone_number validation & harmonization(make consistent)
            if not phone_number_regex.match(data['phone_number']):
                return JsonResponse({'message': 'INPUT ERROR'}, status=400)

            # nickname blank check
            if len(data['nickname']) == 0:
                raise IntegrityError

            # POST
            User.objects.create(
                account      = data['account'],
                password     = password_decoded,
                phone_number = data['password'],
                nickname     = data['nickname']
                )
            return JsonResponse({'message':'CREATED'}, status=201)
        
        except KeyError:
            return JsonResponse({'message':'KEY ERROR'}, status=400)

        except ValueError:
            return JsonResponse({'message': 'INPUT ERROR'}, status=400)

        except IntegrityError:
            return JsonResponse({'message':'INPUT ERROR'}, status=400)

class UserSigninView(View):
    def get(self, request):
        try:
            data = json.loads(request.body)
            user = User.objects.get(account=data['account'])

            if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message':'INVALID USER'}, status=401)

            payload = {'account': user.account}
            token = jwt.encode(payload, SECRET_KEY, ALGORYTHM)            
            return JsonResponse({'message':'SUCCESS','token':token}, status=200)

        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID USER'}, status=401)
        
        except KeyError:
            return JsonResponse({'message': 'KEY ERROR'}, status=400)



