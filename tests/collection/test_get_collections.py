import json

from tests.api_test_case import APITestCase
from tests.factory import Factory


class GetCollectionTest(APITestCase):
    def setUp(self, **kwargs):
        super(GetCollectionTest, self).setUp()

        self._factory = Factory()
        self._user = self._factory.create_user()
        self._user_token = self._factory.login_user(self._user)
        self._other_user = self._factory.create_user(email='user@user.com')
        self._other_user_token = self._factory.login_user(self._other_user)

    def _url(self, collection_id):
        return f'/api/collections/{collection_id}'

    def test_get_created_collection_by_id(self):
        # Given
        collection_id = self._factory.create_collection_with(self._user)

        # When
        response = self.app.get(self._url(collection_id), headers={
                                'Authorization': self._user_token})

        # Then
        self.assertEqual(200, response.status_code)
        json_response = json.loads(response.data)
        self.assertEqual(json_response['object']['id'], collection_id)

    def test_if_user_not_owner_then_cant_see_the_collection(self):
        # Given
        collection_id = self._factory.create_collection_with(self._user)

        # When
        response = self.app.get(self._url(collection_id), headers={
                                 'Authorization': self._other_user_token})

        # Then
        self.assertEqual(500, response.status_code)
        self.assertTrue(json.loads(response.data)['errors'])


