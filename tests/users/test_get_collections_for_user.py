import json

from tests.api_test_case import APITestCase
from tests.factory import Factory


class GetUserCollectionTest(APITestCase):
    def setUp(self, **kwargs):
        super(GetUserCollectionTest, self).setUp()

        self._factory = Factory()
        self._user = self._factory.create_user()
        self._user_token = self._factory.login_user(self._user)
        self._other_user = self._factory.create_user(email='user@user.com')
        self._other_user_token = self._factory.login_user(self._other_user)

    def _url(self):
        return f'/api/users/collections'

    def test_get_user_collections_return_all_created_collections(self):
        # Given
        user_collection_id = self._factory.create_collection_with(self._user)

        # When
        response = self.app.get(self._url(), headers={
                                'Authorization': self._user_token})

        # Then
        self.assertEqual(200, response.status_code)
        json_response = json.loads(response.data)
        self.assertEqual(len(json_response['object']), 1)
        self.assertEqual(json_response['object'][0]['id'], user_collection_id)

    def test_get_user_collections_return_empty_result_when_collection_not_created(self):
        # Given
        self._factory.create_collection_with(self._user)

        # When
        response = self.app.get(self._url(), headers={
                                'Authorization': self._other_user_token})

        # Then
        self.assertEqual(200, response.status_code)
        json_response = json.loads(response.data)
        self.assertEqual(len(json_response['object']), 0)
