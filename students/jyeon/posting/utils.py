import jwt
import json

from django.http.response import JsonResponse

from mysettings           import ALGORYTHM, SECRET_KEY
from user.models          import User

def authorize_account(func):
    def wrapper(self, request):
        try:
            data_headers = request.headers['Authorization']
            data_body    = json.loads(request.body)
            prefix       = 'Bearer \"'
            suffix       = '\"'

            if not data_headers.startswith(prefix):
                return JsonResponse({'message':'NO AUTHORIZATION TOKEN IN REQUEST'})
            
            data_headers         = data_headers[len(prefix):-len(suffix)]
            auth                 = jwt.decode(data_headers, SECRET_KEY, ALGORYTHM)                
            auth_account         = User.objects.get(account=auth['account'])
            
            if not data_body['account'] == auth_account.account:
                return JsonResponse({'message':'INVALID USER'}, status=401)    
            
            result  = func(self,request, auth_account)
            return result

        except KeyError:
            return JsonResponse({'message':'KEY ERROR'}, status=400)

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message':'FAIL TO DECODE TOKEN'}, status=400)
        
        except jwt.exceptions.InvalidSignatureError:
            return JsonResponse({'message':'INVALID USER'}, status=401)    
        
        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID USER'}, status=401)
            
    return wrapper

