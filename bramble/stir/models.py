from django.db import models
from django.contrib.postgres.fields.jsonb import JSONField
import uuid


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
  measurements = JSONField()
  glass = JSONField()
  guid = models.UUIDField(default=uuid.uuid4,
         editable=False)

  class Meta:
    db_table = 'cocktails_2'
    managed = False
