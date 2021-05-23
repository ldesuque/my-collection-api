import json

from tests.api_test_case import APITestCase
from tests.factory import Factory
from documents.sessions import SessionsCollection


class EditCollectionTest(APITestCase):
    def setUp(self, **kwargs):
        super(EditCollectionTest, self).setUp()

        self._factory = Factory()
        self._user = self._factory.create_user()
        self._user_token = self._factory.login_user(self._user)
        self._other_user = self._factory.create_user(email='user@user.com')
        self._other_user_token = self._factory.login_user(self._other_user)
        
    def _url(self, collection_id):
        return f'/api/collections/edit/{collection_id}'

    def test_if_user_is_owner_then_can_edit(self):
        # Given
        original_name = "Private collection"
        new_name = "My private collection edited"
        collection_id = self._factory.create_collection_with(
            self._user, original_name)

        # When
        response = self.app.post(self._url(collection_id), json={'name': new_name}, headers={
                                 'Authorization': self._user_token})

        # Then
        self.assertEqual(200, response.status_code)
        self.assertFalse(json.loads(response.data)['errors'])

    def test_if_user_not_owner_then_cant_edit(self):
        # Given
        original_name = "Private collection"
        new_name = "My private collection edited"
        collection_id = self._factory.create_collection_with(
            self._user, original_name)

        # When
        response = self.app.post(self._url(collection_id), json={'name': new_name}, headers={
                                 'Authorization': self._other_user_token})

        # Then
        self.assertEqual(500, response.status_code)
        self.assertTrue(json.loads(response.data)['errors'])
