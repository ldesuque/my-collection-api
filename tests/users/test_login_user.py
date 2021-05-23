import json
from app import app
from database import mongo
from tests.api_test_case import APITestCase
from tests.factory import Factory

from documents.users import UsersCollection


class LoginUserTest(APITestCase):
    def setUp(self, **kwargs):
        super(LoginUserTest, self).setUp()
        self._factory = Factory()

    def _url(self):
        return f'/api/users/add-and-login'

    def test_login_user_if_data_is_valid_then_the_user_is_added(self):
        # Given
        user_data = self._factory.generate_user_data()

        # When
        response = self.app.post(self._url(), json=user_data)

        # Then
        self.assertEqual(201, response.status_code)
        self.assertIn('token', json.loads(response.data)['object'])
        self.assertIsNotNone(UsersCollection().find_one(
            {'email': user_data['email']}))

    def test_login_user_incomplete_data_then_user_is_not_created(self):
        # Given
        user_data = self._factory.generate_user_data()
        user_data.pop('email')

        # When
        response = self.app.post(self._url(), json=user_data)

        # Then
        self.assertEqual(500, response.status_code)
        self.assertTrue(json.loads(response.data)['errors'])
        self.assertIn("email", json.loads(response.data)['errors'][0])

    def test_login_user_if_theres_an_additional_field_user_not_created(self):
        # Given
        user_data = self._factory.generate_user_data()
        additional_field = 'surname'
        user_data[additional_field] = 'Gonzalez'

        # When
        response = self.app.post(self._url(), json=user_data)

        # Then
        self.assertEqual(500, response.status_code)
        self.assertTrue(json.loads(response.data)['errors'])
        self.assertIn(additional_field, json.loads(response.data)['errors'][0])
        
    def test_if_invalid_password_then_not_login(self):
        # Given
        self._factory.create_user(email="abc@test.com", password="correct")
        user_data = self._factory.generate_user_data(email="abc@test.com", password="invalid")
        
        # When
        response = self.app.post(self._url(), json=user_data)
        
        # Then
        self.assertEqual(500, response.status_code)
        self.assertTrue(json.loads(response.data)['errors'])
        
        
