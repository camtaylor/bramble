from django.urls import path
from django.conf.urls import url
from profiles.views import UserProfileView


urlpatterns = [
    path('user/', UserProfileView.as_view()),
]