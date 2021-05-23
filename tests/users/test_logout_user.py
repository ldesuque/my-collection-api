from documents.sessions import SessionsCollection
from documents.users import UsersCollection
from tests.factory import Factory
from tests.api_test_case import APITestCase


class LogoutUserTest(APITestCase):
    def setUp(self, **kwargs):
        super(LogoutUserTest, self).setUp()

    def _url(self):
        return '/api/users/logout'

    def test_if_token_is_correct_the_session_is_deleted(self):
        # Given
        factory = Factory()
        user = factory.create_user()
        token = factory.login_user(user=user)

        # When
        response = self.app.post(self._url(), headers={'Authorization': token})

        # Then
        self.assertEqual(200, response.status_code)
        self.assertIsNone(SessionsCollection().find_one(token))
