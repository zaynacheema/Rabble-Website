from rest_framework import serializers
from rabble.models import Post, SubRabble
from django.contrib.auth import get_user_model

User = get_user_model()

class SubRabbleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubRabble
        fields = ['id', 'name', 'description', 'anonymous_post', 'visibility', 'num_posts']

class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )
    subrabble = serializers.SlugRelatedField(
        queryset=SubRabble.objects.all(),
        slug_field='id'
    )
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'author', 'subrabble', 'like_count']

    def get_like_count(self, obj):
        return obj.likes.count()
