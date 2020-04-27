from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('cocktails/', views.all_cocktails),
    path('cocktails/<str:search_string>/', views.cocktail_search),
    path('ingredients/<str:search_string>/', views.ingredient_search),
]

urlpatterns = format_suffix_patterns(urlpatterns)