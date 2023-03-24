import json
from datetime import datetime

from django.test import TestCase
from rest_framework.test import APIClient

import mongomock
from unittest.mock import patch

client = APIClient()

mock_client = mongomock.MongoClient()
testdb = mock_client['testdb']
test_posts_collection = testdb['posts']

# Patch the pymongo.MongoClient class with your mongomock.MongoClient instance
patcher = patch('pymongo.MongoClient', return_value=mock_client)
patcher.start()


class PostViewTestCase(TestCase):

    # def setUp(self):
    #     self.initial_post = {"topics": ["web-design"],
    #                         "body": "Post about design, some useful info just tp test how this sing works"}
    #     posts_collection.insert_one(self.initial_post)

    def test_POST(self):
        data = {"topics": ["web-design"], "body": "Post about design"}
        response = self.client.post('/api/posts/', data=json.dumps(data), content_type='application/json')
        self.assertEqual(len(response.data), 24)
        self.assertEqual(response.status_code, 200)

    def test_GET(self):
        post_upload_time = datetime.utcnow()

        self.initial_post = {"topics": ["web-design"],
                            "body": "Post about design, some useful info just to test how this sing works",
                            "upload_time": post_upload_time}

        test_posts_collection.insert_one(self.initial_post)

        post_id = self.initial_post["_id"]
        response = self.client.get(f'/api/posts/{str(post_id)}/')

        self.assertEqual(response.data,
                         {
                             "post": [
                                 {
                                     "topics": [
                                         "web-design"
                                     ],
                                     "body": "Post about design, some useful info just to test how this sing works",
                                     "upload_time": str(self.initial_post['upload_time'])[:-3] + '000'
                                 }
                             ]
                         })
