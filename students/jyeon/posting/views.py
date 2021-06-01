import json
import jwt

from django.views import View
from django.http  import JsonResponse

from mysettings   import ALGORYTHM, SECRET_KEY
from .models      import Posting
from user.models  import User

def authorize_account(func):
    def wrapper(self, request):
        data = json.loads(request.body)
        auth = jwt.decode(data['token'], SECRET_KEY, ALGORYTHM)
        auth_account = User.objects.get(account=auth['account'])
        if auth_account:
            result = func(self, request, auth_account)
        return result
    return wrapper

class PostingView(View):
    @authorize_account
    def post(self, request, auth_account):
        data = json.loads(request.body)
        # # user = User.objects.get(account=data['account'])
        # images = data['image']
        # for i in images:
        #     Posting.objects.create(account=auth_account, image=i, text = data['text'])
        return JsonResponse({'message':'SUCCESS'}, status=201)

    def get(self, request):
        data = json.loads(request.body)
        user = User.objects.get(account=data['account'])

        result = {}
        result_list = []        
        
        for posting in Posting.objects.filter(account = user):
            result = {
                'image':posting.image,
                'text':posting.text,
                'datetime':posting.datetime
            }
            result_list.append(result)
        
        return JsonResponse({'message':result_list}, status=200)
        
# class UserView(View):
#     def post(self, request):
#         return JsonResponse({'message':'SUCCESS'}, status=200)


# class UserSignupView(View):

#     def post(self, request):

#         try:
#             data                = json.loads(request.body)
            
#             account_regex       = re.compile('^[A-Za-z0-9\.+_-]+\@[A-Za-z0-9\._-]+\.[a-zA-Z]+$')
#             phone_number_regex1 = re.compile('^[0-9]{3}[0-9]{3,4}[0-9]{3,4}$')
#             phone_number_regex2 = re.compile('^[0-9]{3}\-[0-9]{3,4}\-[0-9]{3,4}$')
            
#             # account null check & validation
#             if len(data['account']) == 0:
#                 raise ValueError
#             elif not account_regex.match(data['account']):
#                 return JsonResponse({'message':'INPUT ERROR'}, status=400)
            
#             # password null check & validation
#             if len(data['password']) == 0:
#                 raise ValueError
#             elif len(data['password']) < 8:
#                 return JsonResponse({'message': 'INPUT ERROR'}, status=400)
            
#             # phone_number null check
#             if len(data['phone_number']) == 0:
#                 raise ValueError

#             # phone_number validation & harmonization(make consistent)
#             if phone_number_regex1.match(data['phone_number']):
#                 phone_number = data['phone_number']                
#             elif phone_number_regex2.match(data['phone_number']):
#                 phone_number = data['phone_number'].replace('-','')
#             else:
#                 return JsonResponse({'message': 'INPUT ERROR'}, status=400)

#             # nickname validation
#             if len(data['nickname']) == 0:
#                 raise ValueError

#             # POST
#             User.objects.create(
#                 account      = data['account'],
#                 password     = data['password'],
#                 phone_number = phone_number,
#                 nickname     = data['nickname']
#             )            
#             return JsonResponse({'message':'CREATED'}, status=201)
        
#         except KeyError:
#             return JsonResponse({'message':'KEY ERROR'}, status=400)
        
#         except IntegrityError:
#             return JsonResponse({'message': 'ACCOUNT or PHONE NUMBER or NICK NAME ALEADY EXISTS'}, status=409)

#         except ValueError:
#             return JsonResponse({'message': 'VALUE ERROR'}, status=400) # 조건에 맞지 않게 입력했을 경우와, 내용을 입력하지 않았을 경우를 구분할 것인가?
# from django.shortcuts import render

# # Create your views here.
