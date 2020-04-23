from django.contrib import admin

# Register your models here.

from .models import Cocktail

admin.site.register(Cocktail)
