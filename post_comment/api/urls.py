from django.urls import path
from .views import PostView

urlpatterns = [
    path('api/posts/<str:pk>/', PostView.as_view(), name='post-view'),
    path('api/posts/', PostView.as_view(), name='posts-view')
    ]
