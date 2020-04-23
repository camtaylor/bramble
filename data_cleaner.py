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
  cocktails = load_file("cocktail_list.json")
  no_glassware = []
  glassware = []
  new_cocktails = []
  for cocktail in cocktails:

    instructions = " ".join(cocktail["instructions"])
    instructions = instructions.replace(" an ", " a ")
    instructions = instructions.replace("mixing glass", "")
    instructions = instructions.replace("chilled", "")
    instructions = instructions.replace("filled with fresh ice", "")
    instructions = instructions.replace("ice-filled", "")
    instructions = instructions.replace("prepared", "")
    instructions = instructions.lower()


    glass = re.findall("(?<=into a)[^\.]*? glass", instructions)
    if len(glass) == 0:
      glass = re.findall("(?<=into the )[^\.]*? glass", instructions, re.IGNORECASE)
    if "old fashioned glass" in instructions:
      glass = ["old fashioned glass"]
    if "collins glass" in instructions:
      glass = ["collins glass"]
    if "coupe" in instructions:
      glass = ["coupe glass"]
    if "cocktail glass" in instructions:
      glass = ["cocktail glass"]
    if "highball glass" in instructions:
      glass = ["highball glass"]
    if "champagne flute" in instructions:
      glass = ["champagne flute"]
    if "rocks glass" in instructions:
      glass = ["rocks glass"]
    if "pint glass" in instructions:
      glass = ["pint glass"]
    if len(glass) == 0:
      glass = re.findall("(?<=rim of a)[^\.]*? glass", instructions, re.IGNORECASE)
    if len(glass) == 0:
      glass = re.findall("(?<=to a )[^\.]*? glass", instructions)
    if len(glass) == 0:
      glass = re.findall("flute", instructions, re.IGNORECASE)
    if len(glass) == 0:
      glass = re.findall("teacup", instructions, re.IGNORECASE)
    if len(glass) == 0:
      glass = re.findall("punch bowl", instructions, re.IGNORECASE)
    if len(glass) == 0:
      glass = re.findall("mug", instructions, re.IGNORECASE)
    if len(glass) == 0:
      glass = re.findall("pint glass", instructions, re.IGNORECASE)
    if len(glass) == 0:
      glass = re.findall("snifter", instructions, re.IGNORECASE)
    if len(glass) == 0:
      glass = re.findall("(?<= a )[^\.]*? glass", instructions, re.IGNORECASE)
    if len(glass) == 0:
      glass = re.findall("julep cup", instructions, re.IGNORECASE)
    if len(glass) == 0:
      glass = re.findall("shot glass", instructions, re.IGNORECASE)
    if len(glass) == 0:
      glass = re.findall("(?<=into the )[^\.]*? glass", instructions, re.IGNORECASE)
    if len(glass) == 0:
      glass = re.findall("(?<=a )[^\.]*? cup", instructions, re.IGNORECASE)
    if len(glass) == 0:
      glass = re.findall("(?<=into)[^\.]*? glass", instructions, re.IGNORECASE)
    if "shot" in cocktail["name"].lower():
      glass = ["shot glass"]
    if "goblet" in instructions:
      glass = ["goblet"]
    if "rocks glass" in instructions:
      glass = ["rocks glass"]
    if "pitcher" in instructions:
      glass = ["pitcher"]
    if "punch cup" in instructions:
      glass = ["punch cup"]
    if "Mason jar" in instructions:
      glass = ["mason jar"]
    if "syrup" in cocktail["name"].lower():
      continue
    if len(glass) == 0:
      no_glassware.append(cocktail["name"])

    glass = list(set([g.strip().lower() for g in glass]))
    cocktail["glass"] = glass
    new_cocktails.append(cocktail)
    glassware.extend([g.strip().lower() for g in glass])

  counter = Counter(glassware)
  pprint.pprint(random.choice(new_cocktails))
  with open("liquor_list.json", 'w') as f:
    f.write(json.dumps(new_cocktails, indent=4))