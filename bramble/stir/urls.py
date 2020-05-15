from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
  path('', views.APIDirectory.as_view(), name='stir_directory'),
  path('cocktail/<str:id>', views.CocktailCursor.as_view(), name='cursor'),
  path('search/', views.CocktailSearch.as_view(), name='cocktail_search'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
