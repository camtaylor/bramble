from django.contrib import admin

from .models import BrambleUserProfile
from .models import CocktailProfile

admin.site.register(BrambleUserProfile)
admin.site.register(CocktailProfile)