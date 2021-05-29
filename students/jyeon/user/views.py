import json
import re

from django.views import View
from django.http import JsonResponse
from django.db import IntegrityError

from .models import User

class UserSignupView(View):

    def post(self, request):

        try:
            data                = json.loads(request.body)
            
            account_regex       = re.compile('^[A-Za-z0-9\.+_-]+\@[A-Za-z0-9\._-]+\.[a-zA-Z]+$')
            phone_number_regex1 = re.compile('^[0-9]{3}[0-9]{3,4}[0-9]{3,4}$')
            phone_number_regex2 = re.compile('^[0-9]{3}\-[0-9]{3,4}\-[0-9]{3,4}$')
            
            # account null check & validation
            if len(data['account']) == 0:
                raise ValueError
            elif not account_regex.match(data['account']):
                return JsonResponse({'message':'INPUT ERROR'}, status=409)
            
            # password null check & validation
            if len(data['password']) == 0:
                raise ValueError
            elif len(data['password']) < 8:
                return JsonResponse({'message': 'INPUT ERROR'}, status=409)
            
            # phone_number null check
            if len(data['phone_number']) == 0:
                raise ValueError

            # phone_number validation & harmonization(make consistent)
            if phone_number_regex1.match(data['phone_number']):
                phone_number = data['phone_number']                
            elif phone_number_regex2.match(data['phone_number']):
                phone_number = data['phone_number'].replace('-','')
            else:
                return JsonResponse({'message': 'INPUT ERROR'}, status=409)

            # nickname validation
            if len(data['nickname']) == 0:
                raise ValueError

            # POST
            User.objects.create(
                account      = data['account'],
                password     = data['password'],
                phone_number = phone_number,
                nickname     = data['nickname']
            )            
            return JsonResponse({'message':'CREATED'}, status=201)
        
        except KeyError:
            return JsonResponse({'message':'KEY ERROR'}, status=409)
        
        except IntegrityError:
            return JsonResponse({'message': 'ACCOUNT or PHONE NUMBER or NICK NAME ALEADY EXISTS'}, status=409)

        except ValueError:
            return JsonResponse({'message': 'VALUE ERROR'}, status=409)