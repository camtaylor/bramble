from rest_framework import serializers
from .models import Cocktail


class CocktailSerializer(serializers.ModelSerializer):


    class Meta:
      model = Cocktail
      fields = ['name', 'ingredients', 'instructions', 'garnishes', 'glass', '_links']