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
        post = posts_collection.find({'_id': ObjectId(pk)})

        if post:
            for item in post:
                resp = {'post': [{'user_id': item['user_id']}, {'topics': item['topics']},
                                 {'body': item['body']}, {'upload_time': str(item['upload_time'])}]}
                return Response(resp, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        print(request.body)

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
            'user_id': {
                'type': 'integer',
                'required': True
            },
            'upload_time': {
                'required': True
            }
        }

        v = Validator(schema)

        data = json.loads(request.body.decode('utf-8'))

        data['user_id'] = 21
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