from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token



class BrambleTestCase(APITestCase):

  """
  Base class for bramble test cases. This imports 'initial_data.json' to populate the test db.
  """

  fixtures = ['intial_data.json']


  def login(self):
    try:
      user = User.objects.get_by_natural_key("test")
    except Exception as e:
      user = User.objects.create_user(username="test")
      user.set_password('testpassword')
      user.is_staff = True
      user.save()
    self.client.login(username="test", password="testpassword")




class CocktailCursorTest(BrambleTestCase):
  """
  Test case for obtaining a single cocktail at a cursor.
  """
  def test_cursor(self):
    response = self.client.get('/stir/cocktail/43')
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    self.login()
    response = self.client.get('/stir/cocktail/43')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    print(response.data)


class CocktailSearchTest(BrambleTestCase):
  """
  Test case to return results of a search query.
  """
  def test_search(self):
    response = self.client.get('/stir/search/white russian/')
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    self.login()
    response = self.client.get('/stir/search/white russian/')
    self.assertEqual(response.status_code, status.HTTP_200_OK)