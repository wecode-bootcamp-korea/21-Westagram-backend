from django.urls import path
from.views       import PostView

urlpatterns = [
    path('/posting',PostView.as_view()),

]
