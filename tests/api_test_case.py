import unittest

from app import app
from database import mongo


class APITestCase(unittest.TestCase):
    def setUp(self, with_default_categories=True):
        self.app = app.test_client()
        self.db = mongo.db

    def tearDown(self):
        # Delete collections after the test is complete
        for collection in self.db.list_collection_names():
            self.db.drop_collection(collection)