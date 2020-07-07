import json
from collections import Counter
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
import numpy as np
import pandas as pd


def get_cocktail_list(filename):
  """
  Function to convert text file in JSON format to list of dictionaries.


  :param filename:
  :return:
  """
  cocktail_list = []
  with open(filename) as f:
    file_string = f.read()
    cocktail_list = json.loads(file_string)
  return cocktail_list


def get_ingredients_list(cocktail_list):
  """

  Function that returns a list of lists containing ingredients from each cocktail.

  :param cocktail_list: (list) List of each cocktail (dictionary)
  :return:
  """
  return [cocktail["ingredients"] for cocktail in cocktail_list]


def get_cocktail(cocktail_list, name):
  """

  :param cocktail_list:
  :param name:
  :return:
  """
  return next(item for item in cocktail_list if item["name"] == name)


def get_coincidence_frame(coincidence_list):
  """

  Function to tally coincidence of an element in a group. Ingredients rows by ingredients column frame.

  :param coincidence_list:
  :return:
  """
  u = (pd.get_dummies(pd.DataFrame(coincidence_list), prefix='', prefix_sep='')
    .groupby(level=0, axis=1)
    .sum())
  v = u.T.dot(u)
  return v


def get_cocktail_frame(cocktails):
  """

  Function to create a binary matrix (pandas data frame) for cocktails rows by
  ingredient columns.

  :param cocktails:
  :return: cocktail_frame (pandas data frame)
  """
  mlb = MultiLabelBinarizer()
  cocktail_frame = pd.DataFrame(mlb.fit_transform(cocktails.values()),
                                 columns=mlb.classes_,
                                 index=cocktails.keys())
  return cocktail_frame


def query_by_ingredient(cocktail_frame, ingredient):
  """

  Function to build a frame with all cocktail vectors that contain an ingredient.

  :param cocktail_frame: (pandas data frame)
  :param ingredient: (string)
  :return: (pandas data frame)
  """
  return cocktail_frame.loc[cocktail_frame[ingredient] == 1]


def query_by_cocktail(cocktail_frame, cocktail_name):
  """

  Function to build a frame with all ingredient vectors that are in a cocktail.

  :param cocktail_frame:
  :param cocktail_name:
  :return:
  """
  return cocktail_frame.loc[:,cocktail_frame.loc[cocktail_name]>0]


def get_cocktail_series(cocktail_frame, cocktail_name):
  """

  :param cocktail_frame:
  :param cocktail_name:
  :return:
  """
  return cocktail_frame.loc[[cocktail_name]]


def get_cocktail_vector(cocktail_frame, cocktail_name):
  """

  :param cocktail_frame: (pandas data frame) cocktails by ingredients data frame
  :param cocktail_name: (string) the name of a cocktail i.e. "old fashioned"
  :return: (pandas data series) a sum of all the ingredient vectors in the cocktail
  """
  frame = query_by_cocktail(cocktail_frame, cocktail_name)
  return frame.sum(axis=1)


def cocktail_cosine(cocktail_frame1,cocktail_frame2):
  """

  :param cocktail_frame1: (pandas data frame)
  :param cocktail_frame2: (pandas data frame)
  :return: (float) cosine similarity between two vectors
  """
  return cosine_similarity(cocktail_frame1.values.reshape(1, -1),
                    cocktail_frame2.values.reshape(1, -1))


if __name__ == "__main__":

  cocktail_json = get_cocktail_list("bramble_list.json")
  cocktail_index = {}
  ingredients = defaultdict(list)
  ingredient_vectors = {}


  for index, cocktail in enumerate(cocktail_json):
    ingredient_list = [ingredient["ingredient"] for ingredient in cocktail["measured_ingredients"]]
    cocktail_index[cocktail["name"]] = index
    for ingredient in ingredient_list:
      ingredients[ingredient].append(index)

  for ingredient, indices in ingredients.items():
    ingredient = ingredient.strip().lower()
    ingredient_vectors[ingredient] = np.zeros(len(cocktail_json), dtype=np.bool)
    ingredient_vectors[ingredient][indices] = True

  data_frame = pd.DataFrame.from_dict(ingredient_vectors)