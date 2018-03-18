from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory, APIClient, force_authenticate
from .user_setup import setup_user

from polls import views


class TestPoll(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.user = setup_user()
        # self.post_view = views.PollViewSet.as_view({'post'})
        self.view = views.PollViewSet.as_view({'get': 'list', 'post': 'create'})
        self.uri = '/polls/'
    
    def test_get(self):
        # params = {'get': 'list'}
        request = self.factory.get(self.uri)
        force_authenticate(request, self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, recieved {0} instead.'
                         .format(response.status_code))
    
    def test_post_uri(self):
        params = {
            "question": "How are you man?",
            "choice_strings": ["Yo man", "Not Fine"],
            "created_by": 1
        }
        request = self.factory.post(self.uri, params)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, 201,
                         'Expected Response Code 201, recieved {0} instead.'
                         .format(response.status_code))
