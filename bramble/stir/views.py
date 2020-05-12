from .models import Cocktail
from .serializers import CocktailSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import PageNumberPagination
from django.contrib.postgres.search import TrigramSimilarity

from django.db import connection
with connection.cursor() as cursor:
  cursor.execute('CREATE EXTENSION IF NOT EXISTS pg_trgm')

class BrambleAPIView(APIView, PageNumberPagination):
  """
  This class will serve as a base class from which all other APIViews will inherit.

  Functions this view will eventually implement:

  User auth
  Rate limiting
  Usage statistic monitoring
  Other functions as needed

  """
  # For now, only allow admin to access api.
  permission_classes = [IsAdminUser]

  def get_paginated_response(self, data):

    response_dict = {
      '_links': {
        'self': {'href': self.request.build_absolute_uri()}
      },
      'count': self.page.paginator.count,
      'results': data
    }

    next_page = self.get_next_link()
    prev_page = self.get_previous_link()

    if next_page is not None:
      response_dict['_links']['next'] = {'href': next_page}
    if prev_page is not None:
      response_dict['_links']['previous'] = {'href': prev_page}


    return Response(response_dict)


class CocktailCursor(BrambleAPIView):
  """
  Class to return a single cocktail by id. Currently uses an in order integer by order inserted into db.

  TODO: Change id to a hashed representation so database can not be iterated.
  """

  def get(self, request, id):
    cocktail = Cocktail.objects.get(id=id)
    serializer = CocktailSerializer(cocktail, context={'request': request})
    return Response(serializer.data)


class CocktailSearch(BrambleAPIView):
  """
  Search for a cocktail to make based on a given query string.

  TODO: Design a query language to search cocktail DB.
  """

  def get_queryset(self, search_string, request):
    cocktail_search = Cocktail.objects.annotate(similarity=TrigramSimilarity('name', search_string))\
      .filter(similarity__gt=0.3).order_by('-similarity')
    return self.paginate_queryset(cocktail_search, request)

  def get(self, request):

    # Get Search string from parameters
    #TODO check if param exists.
    search_string = request.GET["search"]



    cocktail_search = self.get_queryset(search_string, request)
    serializer = CocktailSerializer(cocktail_search, many=True, context={'request': request})
    return self.get_paginated_response(serializer.data)


class IngredientSearch(BrambleAPIView):
  """
  Search for cocktails containing an ingredient.

  TODO: Remove class and include ingredient search in "Cocktail Search"
  TODO: Make sorting for ingredients similarity.
  """

  def get_queryset(self, search_string, request):
    cocktail_search = Cocktail.objects.filter(ingredients__icontains=search_string)
    return self.paginate_queryset(cocktail_search, request)

  def get(self, request, search_string):
    cocktail_search = self.get_queryset(search_string, request)
    serializer = CocktailSerializer(cocktail_search, many=True, context={'request': request})
    return self.get_paginated_response(serializer.data)
