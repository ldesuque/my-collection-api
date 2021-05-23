import json
import ndjson

from tests.api_test_case import APITestCase
from tests.factory import Factory
from documents.sessions import SessionsCollection

ndjson_file = "./data/sample_moodboard.ndjson"


class CustomCollectionTest(APITestCase):
    def setUp(self, **kwargs):
        super(CustomCollectionTest, self).setUp()

        self._factory = Factory()
        self._user = self._factory.create_user()
        self._user_token = self._factory.login_user(self._user)
        self._other_user = self._factory.create_user(email='user@user.com')
        self._other_user_token = self._factory.login_user(self._other_user)
        
        self._initialize_data()

    def _initialize_data(self):
        try:
            with open(ndjson_file) as f:
                data = ndjson.load(f)
            
            self.db['moodboards'].insert_many(data)
        except Exception as error:
            print('Data initializer error: ' + str(error))

    def _url(self, collection_id):
        return f'/api/collections/custom/{collection_id}'

    def test_owner_can_add_image_to_his_collection(self):
        # Given
        collection_id = self._factory.create_collection_with(self._user)
        trend_data = self._factory.get_valid_trend_data()
        
        # When
        response = self.app.post(self._url(collection_id), json=trend_data, headers={
                                 'Authorization': self._user_token})

        # Then
        self.assertEqual(200, response.status_code)
        self.assertFalse(json.loads(response.data)['errors'])

    def test_owner_can_delete_image_from_his_collection(self):
        # Given
        collection_id = self._factory.create_collection_with(self._user)
        image_data = self._factory.get_valid_image_data()
        
        # When
        response = self.app.delete(self._url(collection_id), json=image_data, headers={
                                 'Authorization': self._user_token})

        # Then
        self.assertEqual(200, response.status_code)
        self.assertFalse(json.loads(response.data)['errors'])

    def test_invited_cant_add_image_to_the_collection(self):
        # Given
        collection_id = self._factory.create_collection_with(self._user)
        trend_data = self._factory.get_valid_trend_data()
        
        # When
        response = self.app.post(self._url(collection_id), json=trend_data, headers={
                                 'Authorization': self._other_user_token})

        # Then
        self.assertEqual(500, response.status_code)
        self.assertTrue(json.loads(response.data)['errors'])
