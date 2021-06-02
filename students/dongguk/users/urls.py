from django.urls import path
from .views      import SignupView
 

urlpatterns = [
    path('', SignupView.as_view())
]

# /users
# 어떤 일을 처리해야 할지 로직
#from .views      import SignupView >>>> 내가 views 폴더안에 있는 SignupView 을 불러온다는 뜻