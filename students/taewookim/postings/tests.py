import json, bcrypt, copy

from django.test    import TestCase, Client
from unittest.mock  import patch, MagicMock

from .models      import Posting, PostingImage
from users.models import User

class PostingTest(TestCase):
    def setUp(self):
        User.objects.create(
            email        = 'test@wecode.com', 
            password     = '12345678', 
            nickname     = '타식', 
            phone_number = '010-7777-1234'
        )

        User.objects.create(
            email        = 'test2@wecode.com', 
            password     = '12345678', 
            nickname     = '태식이', 
            phone_number = '010-2345-7890'
        )
    
    def tearDown(self):
        Posting.objects.all().delete()
        PostingImage.objects.all().delete()
        User.objects.all().delete()

    def test_create_and_inquiry_postings(self):
        token      = 'test@wecode.com'
        email      = 'test@wecode.com'
        main_text  = '대신 귀여운 동물을 드리겠습니다'
        image_urls = [
                'https://topclass.chosun.com/news_img/1807/1807_008_1.jpg',
                'http://image.dongascience.com/Photo/2020/03/5bddba7b6574b95d37b6079c199d7101.jpg'
        ]

        posting   = {
                'email'      : email,
                'main_text'  : main_text,
                'image_urls' : image_urls
        } 

        client   = Client()
        response = client.post(
            '/postings', '', 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'NO_BODY_DATA'})

        response = client.post(
            '/postings', json.dumps({'email': email}), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'INVALIED_DATA'})

        no_user_posting          = copy.deepcopy(posting)
        no_user_posting['email'] = 'test'
        response                 = client.post(
            '/postings', json.dumps(no_user_posting), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json(), {'message': 'NO_EXIST_USER'})

        response = client.post(
            '/postings', json.dumps(posting), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message' : 'CREATED'})

        user = User.objects.filter(email=email)
        self.assertEqual(len(user), 1)

        posting = Posting.objects.filter(user=user[0])
        self.assertEqual(len(posting), 1)
        
        for image_url in image_urls:
            self.assertTrue(
                PostingImage.objects.filter(posting=posting[0], 
                url=image_url
                )
            )

        response = client.get('/postings')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'message': [
                    {
                        'user'       : email,
                        'main_text'  : main_text,
                        'image_urls' : image_urls,
                        'created_at' : posting[0].created_at.strftime('%Y-%m-%d %H:%M:%S')
                    },
                ],
            }
        )


