import json
from datetime import datetime
from bson.objectid import ObjectId

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

import pymongo
from cerberus import Validator

client = pymongo.MongoClient('mongodb://xilar:1111@localhost/testdb?authSource=admin')
testdb = client['testdb']
posts_collection = testdb['posts']


class PostView(APIView):

    def get(self, request, pk):
        try:
            post = posts_collection.find_one({'_id': ObjectId(pk)})
            if post:
                resp = {'post': [{'topics': post['topics'],
                                 'body': post['body'], 'upload_time': str(post['upload_time'])}]}
                return Response(resp, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        schema = {
            'topics': {
                'type': 'list',
                'schema': {
                    'type': 'string'
                }
            },
            'body': {
                'type': 'string',
                'required': True
            },
            'upload_time': {
                'required': True
            }
        }

        v = Validator(schema)

        print(type(request.body))
        data = json.loads(request.body.decode('utf-8'))

        data['upload_time'] = datetime.utcnow()

        if v.validate(data):
            posts_collection.insert_one(data)
            return Response(str(data['_id']), status=status.HTTP_200_OK)
        else:
            print(v.errors)
            return Response('incorrect data', status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):  
        try:
            post = posts_collection.delete_one({'_id': ObjectId(pk)})
            if post.deleted_count == 0:
                return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(f'Post {pk} deleted', status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)