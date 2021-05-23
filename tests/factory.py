
from documents.users import UsersCollection
from documents.sessions import SessionsCollection
from documents.collections import CollectionsCollection
from documents.invitations import InvitationsCollection


class Factory:
    def create_user(self, email=None, password=None):
        user_data = self.generate_user_data(email, password)
        UsersCollection().add(user_data)
        return UsersCollection().find_one(user_data)

    @staticmethod
    def generate_user_data(email=None, password=None):
        return {
            'email': email if email else "leandro@desuque.com",
            'password': password if password else 'abc123'
        }

    @staticmethod
    def login_user(user):
        return SessionsCollection().create_for(user)

    def create_collection_with(self, user, name=None):
        collection_data = self.generate_collection_data(name)
        collection_id = CollectionsCollection().add(
            json_data=collection_data, user=user)

        return collection_id

    @staticmethod
    def generate_collection_data(name=None):
        return {'name': "Supreme t-shirt collection" if not name else name}

    def create_invitation_with(self, user_id, invited_id, collection_id):
        InvitationsCollection().add(self.generate_invitation_data(
            invited_id, collection_id), user_id)

    @staticmethod
    def generate_invitation_data(invited_id, collection_id):
        return {"invited_id": invited_id,
                "collection_id": collection_id}

    # Important! *** Refactor ***
    # I am assuming the test database has test data!!!
    # (View app.py file)
    @staticmethod
    def get_valid_trend_data():
        return {"trend_id": "908757787948994295"}

    # Important! *** Refactor ***
    # I am assuming the test database has test data!!!
    # (View app.py file)
    @staticmethod
    def get_valid_image_data():
        return {"md5": "44b791ac5dd454f04681dbc709e3caf9"}