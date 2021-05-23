import json

from tests.api_test_case import APITestCase
from tests.factory import Factory
from documents.collections import CollectionsCollection


class CreateInvitationTest(APITestCase):
    def setUp(self, **kwargs):
        super(CreateInvitationTest, self).setUp()

        self._factory = Factory()
        self._user = self._factory.create_user()
        self._user_token = self._factory.login_user(self._user)
        self._other_user = self._factory.create_user(email='user@user.com')
        self._other_user_token = self._factory.login_user(self._other_user)

    def _url(self):
        return f'/api/invitations'

    def test_owner_invite_other_user_and_they_can_access_to_the_collection(self):
        # Given
        collection_id = self._factory.create_collection_with(self._user)
        invited_id = self._other_user['id']
        invitation_data = self._factory.generate_invitation_data(
            invited_id, collection_id)

        # When
        response = self.app.post(self._url(), json=invitation_data, headers={
            'Authorization': self._user_token})

        # Then
        self.assertEqual(201, response.status_code)
        self.assertFalse(None, CollectionsCollection().get_collection_by_id(
            collection_id, invited_id, invited_allowed=True))
