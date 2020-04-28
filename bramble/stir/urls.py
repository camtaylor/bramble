from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('cocktail/<str:id>', views.CocktailCursor.as_view(), name='cursor'),
    path('search/<str:search_string>/', views.CocktailSearch.as_view(), name='search'),
    path('ingredients/<str:search_string>/', views.IngredientSearch.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)