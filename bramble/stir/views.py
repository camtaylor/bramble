from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Cocktail
from .serializers import  CocktailSerializer
from . import serializers
import nltk

# Create your views here.
@api_view(['GET'])
def all_cocktails(request):
  cocktails = Cocktail.objects.all()
  serializer = CocktailSerializer(cocktails, many=True)
  return Response(serializer.data)

@api_view(['GET'])
def cocktail_search(request, search_string):
  cocktail_search = Cocktail.objects.filter(name__icontains=search_string)
  search_results = list(cocktail_search.all())
  search_results = sorted(search_results, key=lambda cocktail: nltk.edit_distance(cocktail.name, search_string))

  serializer = CocktailSerializer(search_results, many=True)
  return Response(serializer.data)

@api_view(['GET'])
def ingredient_search(request, search_string):
  cocktail_search = Cocktail.objects.filter(ingredients__icontains=search_string)
  search_results = list(cocktail_search.all())
  search_results = sorted(search_results, key=lambda cocktail: nltk.edit_distance(cocktail.name, search_string))

  serializer = CocktailSerializer(search_results, many=True)
  return Response(serializer.data)