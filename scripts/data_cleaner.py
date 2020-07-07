import json
import re
import pprint
from collections import Counter
import random

def load_file(filename):
  cocktail_list = []
  with open(filename) as f:
    cocktail_list = json.loads(f.read())
  return cocktail_list


if __name__ == "__main__":
  cocktails = load_file("./JSON/merged_list.json")
  index = 0
  list_length = len(cocktails)
  for cocktail in cocktails:
    new_cocktail = {}
    ingredients = cocktail["ingredients"][:]
    split_list = [re.split(r'\s(?=[A-Z])', ingredient,1) for ingredient in ingredients]
    measured_ingredients_list = [{"measurement":ingredient[0], "ingredient":ingredient[1]} if len(ingredient) == 2 else {"measurement":"","ingredient":ingredient[-1]} for ingredient in split_list]
    new_cocktail = cocktail
    new_cocktail["measured_ingredients"] = measured_ingredients_list
    with open("bramble_list.json", 'a') as f:
      if index == 0:
        f.write("[\n")
      index += 1
      f.write(json.dumps(new_cocktail, indent=4))

      if index == list_length:
        f.write('\n]')
      else:
        f.write(',\n')