from django.urls import path
from users.views import UserRegistrationView
from users.views import UserLoginView


urlpatterns = [
    path('signup/', UserRegistrationView.as_view()),
    path('login/', UserLoginView.as_view()),
    ]