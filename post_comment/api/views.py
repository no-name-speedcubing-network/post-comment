from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class PostView(APIView):

    def get(self, request, pk):
        return Response(f'You get post {pk}', status=status.HTTP_200_OK)

    def post(self, request):
        return Response('New post created', status=status.HTTP_200_OK)

    def put(self, request, pk):
        return Response(f'Post updated {pk}', status=status.HTTP_200_OK)

    def delete(self, request, pk):
        return Response(f'Post deleted {pk}', status=status.HTTP_200_OK)

