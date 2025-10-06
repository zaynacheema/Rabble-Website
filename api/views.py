from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from django.shortcuts import get_object_or_404
from rabble.models import SubRabble, Post
from .serializers import SubRabbleSerializer, PostSerializer

from django.contrib.auth import get_user_model
User = get_user_model()


@api_view(['GET'])
def subrabble_list(request):
    subrabbles = SubRabble.objects.all()
    serializer = SubRabbleSerializer(subrabbles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def subrabble_detail(request, identifier):
    subrabble = get_object_or_404(SubRabble, id=identifier)
    serializer = SubRabbleSerializer(subrabble)
    return Response(serializer.data)

class PostListCreate(generics.ListCreateAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        identifier = self.kwargs['identifier']
        subrabble = get_object_or_404(SubRabble, id=identifier)
        return Post.objects.filter(subrabble=subrabble)

    def perform_create(self, serializer):
        identifier = self.kwargs['identifier']
        subrabble = get_object_or_404(SubRabble, id=identifier)
        serializer.save(subrabble=subrabble, author=self.request.user)

class PostRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

@api_view(['POST'])
def toggle_like(request, identifier, pk):
    post = get_object_or_404(Post, pk=pk, subrabble__id=identifier)
    username = request.data.get('user')

    if not username:
        return Response({'error': 'User is required'}, status=400)

    user = get_object_or_404(User, username=username)

    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True

    like_count = post.likes.count()

    return Response({'liked': liked, 'like_count': like_count})
