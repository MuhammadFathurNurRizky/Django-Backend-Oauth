from typing import Generic
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import PostSerializer
from .models import Post
from rest_framework import permissions

class CobaView(ListCreateAPIView):
    serializer_class   = PostSerializer
    queryset           = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class CobaDetail(RetrieveUpdateDestroyAPIView):
    serializer_class   = PostSerializer
    queryset           = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field       = "id"

