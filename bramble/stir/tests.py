from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient



class BrambleTestCase(APITestCase):

  """


  TODO: create test table "cocktails" since cocktail model is not managed.
  TODO: write login function to log in as admin.
  """

  def login(self):
    pass



class CocktailCursorTest(BrambleTestCase):
  def test_cursor(self):

    example_output = """
    {
    "name": "'Martini' Thyme",
    "ingredients": [
        "2 sprig   Lemon thyme (remove stalks)",
        "1 oz    Gin",
        ".75 oz   Green Chartreuse",
        ".25 oz    Giffard Sugar Cane Syrup"
    ],
    "instructions": [
        "MUDDLE thyme in base of shaker. Add other ingredients, SHAKE with ice and fine strain into chilled glass."
    ],
    "garnishes": [
        "Olives on thyme sprig"
    ],
    "glass": [
        "Martini glass"
    ]
    }"""


    response = self.client.get('/stir/cocktail/1')
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    self.login()
    response = self.client.get('/stir/cocktail/1')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    print(response.data)