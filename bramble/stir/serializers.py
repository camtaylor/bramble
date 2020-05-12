from rest_framework import serializers
from .models import Cocktail




class CocktailSerializer(serializers.ModelSerializer):


  _links = serializers.SerializerMethodField()

  class Meta:
    model = Cocktail
    fields = ['name', 'ingredients', 'instructions', 'measurements', 'garnishes', 'glass', '_links']


  def get__links(self, obj):
    request = self.context.get('request')
    self_link = request.build_absolute_uri('/stir/cocktail/{}/'.format(obj.id))
    links = {}
    links["self"] = {'href': self_link}
    return links