from .models import Cocktail
from .serializers import CocktailSerializer

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import PageNumberPagination

import nltk




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
    return Response({
      '_links': {
        'next': self.get_next_link(),
        'previous': self.get_previous_link()
      },
      'count': self.page.paginator.count,
      'results': data
    })


class CocktailCursor(BrambleAPIView):
  """
  Class to return a single cocktail by id. Currently uses an in order integer by order inserted into db.

  TODO: Change id to a hashed representation so database can not be iterated.
  """

  def get(self, request, id):
    cocktail = Cocktail.objects.get(id=id)
    serializer = CocktailSerializer(cocktail)
    return Response(serializer.data)


class CocktailSearch(BrambleAPIView):
  """
  Search for a cocktail to make based on a given query string.

  TODO: Design a query language to search cocktail DB.
  TODO: Improve and optimise edit distance/filtering.
  """

  def get_queryset(self, search_string, request):
    cocktail_search = Cocktail.objects.filter(name__icontains=search_string)
    return self.paginate_queryset(cocktail_search, request)

  def get(self, request, search_string):
    cocktail_search = self.get_queryset(search_string, request)
    # search_results = list(cocktail_search.all())
    # search_results = sorted(search_results, key=lambda cocktail: nltk.edit_distance(cocktail.name, search_string))
    serializer = CocktailSerializer(cocktail_search, many=True)
    return self.get_paginated_response(serializer.data)


class IngredientSearch(BrambleAPIView):
  """
  Search for cocktails containing an ingredient.

  TODO: Remove class and include ingredient search in "Cocktail Search"
  """

  def get_queryset(self, search_string, request):
    cocktail_search = Cocktail.objects.filter(ingredients__icontains=search_string)
    return self.paginate_queryset(cocktail_search, request)

  def get(self, request, search_string):
    cocktail_search = self.get_queryset(search_string, request)

    # search_results = list(cocktail_search.all())
    # search_results = sorted(search_results, key=lambda cocktail: nltk.edit_distance(cocktail.name, search_string))

    serializer = CocktailSerializer(cocktail_search, many=True)
    return self.get_paginated_response(serializer.data)
