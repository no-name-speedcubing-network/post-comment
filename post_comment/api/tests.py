from django.test import TestCase
from rest_framework.test import APIClient
import mongomock
from .views import PostView


class PostViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Replace the pymongo.MongoClient instance with a mongomock.MongoClient instance
        self.mock_client = mongomock.MongoClient()
        self.testdb = self.mock_client['testdb']
        self.posts_collection = self.testdb['posts']

        # Patch the posts_collection object in the PostView class to use the mongomock collection
        PostView.posts_collection = self.posts_collection

    def tearDown(self):
        pass

    def test_POST(self):
        # Set up test data

        # Call view being tested
        response = self.client.post('/api/posts/4334/', data={"topics": ["web-design"], "body": "Post about design"})
        print(response.data)
        # Assert expected response
        self.assertEqual(response.status_code, 404)
