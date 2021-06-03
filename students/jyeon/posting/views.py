import json

from django.views          import View
from django.http           import JsonResponse
from django.db             import IntegrityError
from django.core.paginator import Paginator

from mysettings            import ALGORYTHM, SECRET_KEY
from .utils                import authorize_account
from .models               import Posting, Image

class PostingView(View):
    @authorize_account
    def post(self, request, auth_account):
        try:
            data    = json.loads(request.body)

            # Posting table
            posting = Posting.objects.create(
                account      = auth_account,
                posting_text = data['posting_text']
            )
            
            # Image table
            images  = data['posting_image']
            for i in images:
                Image.objects.create(posting_image=i, posting_text=posting)
            
            return JsonResponse({'message':'CREATED'}, status=201)
        
        except KeyError:
            return JsonResponse({'message':'KEY ERROR'}, status=400)
        except ValueError:
            return JsonResponse({'message':'VALUE ERROR'}, status=400)        
        except IntegrityError:
            return JsonResponse({'message':'INTEGRITY ERROR'}, status=400)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'message':'JSON DECODE ERROR'}, status=400)
            


    @authorize_account
    def get(self, request, auth_account):
        try:

            # pagination & get paging index
            pagination  = Paginator(Posting.objects.all(),3)
            page        = int(request.GET.get('page'))

            result      = {}
            result2     = []
            result_list = []        

            # get posting for paging index
            for posting in pagination.page(page):
                result2 = []
                
                for image in Image.objects.filter(posting_text=posting):
                    result2.append(image.posting_image)

                result = {
                    'account':posting.account.account,
                    'datetime':posting.datetime,
                    'text':posting.posting_text,
                    'image': result2
                }
                result_list.append(result)
            
            return JsonResponse({'message':result_list}, status=200)

        except json.decoder.JSONDecodeError:
            return JsonResponse({'message':'JSON DECODE ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message':'KEY ERROR'}, status=400)