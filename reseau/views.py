from rest_framework import generics
from .models import Post
from .serializers import PostSerializer

class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
