from rest_framework.response import Response
from rest_framework.views import APIView
from stir.views import BrambleAPIView
import json





class APIDirectory(BrambleAPIView):
  """
   This view holds a directory to urls that are used in the API.
  """

  def get(self, request):

    link_dict = {

      "cocktail_cursor": "/stir/cocktail/<str:id>",

      "cocktail_search": "/stir/search/<str:search_string>"
    }
    return Response({"_links" : link_dict})