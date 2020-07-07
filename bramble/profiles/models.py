from django.db import models
import uuid
from users.models import BrambleUser
from stir.models import Cocktail


class BrambleUserProfile(models.Model):
  """
  Class to store interactions/metadata by a user.
  """
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  user = models.OneToOneField(BrambleUser, on_delete=models.CASCADE, related_name='profile')



class CocktailProfile(models.Model):
  """
  Class to store interactions/metadata on a cocktail.
  """
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  cocktail = models.OneToOneField(Cocktail, on_delete=models.CASCADE, related_name='profile')
  views = models.PositiveIntegerField(default=1)
  favorites = models.ManyToManyField(BrambleUserProfile, related_name='favorites')
  bookmarks = models.ManyToManyField(BrambleUserProfile, related_name='bookmarks')