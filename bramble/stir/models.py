from django.db import models
from django.contrib.postgres.fields.jsonb import JSONField

# Create your models here.

class Cocktail(models.Model):
  """
    This model holds fields that will be presented in the "stir" app.
    This app is a recipe search app.
  """
  name = models.CharField(max_length=255)
  ingredients = JSONField()
  instructions = JSONField()
  garnishes = JSONField()
  glass = JSONField()

  class Meta:
    managed = False
    db_table = 'cocktails'