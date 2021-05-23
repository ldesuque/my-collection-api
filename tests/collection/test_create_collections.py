import json

from tests.api_test_case import APITestCase
from tests.factory import Factory
from documents.sessions import SessionsCollection


class CreateCollectionTest(APITestCase):
    def setUp(self, **kwargs):
        super(CreateCollectionTest, self).setUp()

        self._factory = Factory()
        self._user = self._factory.create_user()
        self._user_token = self._factory.login_user(self._user)

    def _url(self):
        return '/api/collections'

    def test_if_the_data_is_correct_then_the_collection_is_created(self):
        # Given
        collection_data = self._factory.generate_collection_data()

        # When
        response = self.app.post(self._url(), json=collection_data, headers={
                                 'Authorization': self._user_token})

        # Then
        self.assertEqual(201, response.status_code)
        self.assertFalse(json.loads(response.data)['errors'])
        self.assertIn("id", json.loads(response.data)['object'])

    def test_if_a_field_is_missing_the_collection_not_created(self):
        # Given
        collection_data = self._factory.generate_collection_data()
        collection_data.pop('name')

        # When
        response = self.app.post(self._url(), json=collection_data, headers={
                                 'Authorization': self._user_token})

        # Then
        self.assertEqual(500, response.status_code)
        self.assertTrue(json.loads(response.data)['errors'])
        self.assertIn("name", json.loads(response.data)['errors'][0])

    def test_if_theres_an_additional_field_the_collection_is_not_created(self):
        # Given
        collection_data = self._factory.generate_collection_data()
        additional_field = 'description'
        collection_data[additional_field] = 'My private collection'

        # When
        response = self.app.post(self._url(), json=collection_data, headers={
                                 'Authorization': self._user_token})

        # Then
        self.assertEqual(500, response.status_code)
        self.assertTrue(json.loads(response.data)['errors'])
        self.assertIn(additional_field, json.loads(response.data)['errors'][0])
