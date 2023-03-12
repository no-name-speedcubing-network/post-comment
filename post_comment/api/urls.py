from django.urls import path
from .views import PostView

urlpatterns = [
    path('api/posts/<int:pk>/', PostView.as_view(), name='post-view')
    ]
