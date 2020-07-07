from .models import Cocktail
from .serializers import CocktailSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import PageNumberPagination
from django.contrib.postgres.search import TrigramSimilarity
from django.db import connection
import re
from django.urls import get_resolver
from django.urls import resolve

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

  def build_uri(self, resource):
    """
    Function to build absolute uri from a resource.
    :param request:
    :param resource:
    :return: absolute_uri
    """
    absolute_uri = self.request.build_absolute_uri(resource)
    return absolute_uri

  def build_uri_from_root(self, resource):
    host = self.build_uri("/")
    return host + resource

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


class APIDirectory(BrambleAPIView):
  """
   This view serves to output the structure of the api. This will add in minimal client updates.


  """

  def get_self_link(self):
    return self.build_uri(self.request.path)

  def get_resources(self):
    """
    Function to automatically find descending urls from all urls in the project.

    TODO: Return view code by resolve()?
    TODO: Read view code to provide "params" template
    TODO: Read view code to provide "return" template
    :return:
    """

    root_url = self.get_self_link()
    # Get all url paths from the django project
    all_urls = set(v[1].replace("\\", "").replace("$", "") for k, v in get_resolver(None).reverse_dict.items())
    # Turn paths into hyperlinks
    all_links = [self.build_uri_from_root(url) for url in all_urls]
    # Ensure that links are children of current path
    descending_links = [link for link in all_links if root_url in link and root_url != link]
    # Return only direct children, not grandchildren etc.
    resources = [re.search(r'{}[^/]*/'.format(root_url), link).group(0) for link in descending_links]
    return resources

  def build_directory(self):
    root_url = self.get_self_link()
    link_dict = {}
    link_dict["self"] = {}
    link_dict["self"]["href"] = root_url
    link_dict["resources"] = {}
    resource_dict = link_dict["resources"]
    resources = self.get_resources()
    for resource in resources:
      resource_name = resource.replace(root_url, "")
      resource_dict[resource_name] = {}
      resource_dict[resource_name]["_links"] = {}
      resource_dict[resource_name]["_links"]["self"] = {}
      resource_dict[resource_name]["_links"]["self"]["href"] = self.build_uri(resource_name)

    return {"_links": link_dict}

  def get(self, request):
    directory = self.build_directory()
    return Response(directory)


class CocktailCursor(BrambleAPIView):
  """
  Class to return a single cocktail by id. Currently uses an in order integer by order inserted into db.

  TODO: Change id to a hashed representation so database can not be iterated.
  """

  def get(self, request, id):
    cocktail = Cocktail.objects.get(guid=id)
    serializer = CocktailSerializer(cocktail, context={'request': request})
    return Response(serializer.data)


class CocktailSearch(BrambleAPIView):
  """
  Search for a cocktail to make based on a given query string.

  TODO: Design a query language to search cocktail DB.
  """

  def get_queryset(self, request):

    name = request.query_params.get("name")
    ingredients = request.query_params.get("ingredients")
    cocktails = Cocktail.objects.all()
    if name:
      cocktails = cocktails.annotate(similarity=TrigramSimilarity('name', name)) \
        .filter(similarity__gt=0.3).order_by('-similarity')
    if ingredients:
      ingredients_regex = "^{}.*$".format("".join(
        ["(?=.*{})".format(ingredient) for ingredient in ingredients.split(",")]))

      cocktails = cocktails.filter(ingredients__iregex=ingredients_regex)
    return self.paginate_queryset(cocktails, request)

  def get(self, request):
    """
    :param request:
    :return:
    """
    cocktail_search = self.get_queryset(request)

    serializer = CocktailSerializer(cocktail_search, many=True, context={'request': request})
    return self.get_paginated_response(serializer.data)
