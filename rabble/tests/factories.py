import string
import factory
from factory import Faker, Sequence, SubFactory, post_generation
from factory.django import DjangoModelFactory

from django.contrib.auth import get_user_model
from rabble.models import Community, SubRabble, Post, Comment

User = get_user_model()

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Sequence(lambda n: f'user{n}')
    email = Sequence(lambda n: f'user{n}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'password123')
    bio = Faker('paragraph', nb_sentences=2)
    interests = Faker('words', nb=3)

    @post_generation
    def photo(self, create, extracted, **kwargs):
        pass

class CommunityFactory(DjangoModelFactory):
    class Meta:
        model = Community

class SubRabbleFactory(DjangoModelFactory):
    class Meta:
        model = SubRabble

    id = Sequence(lambda n: f'subr{n}')
    name = Faker('lexify', text='????', letters=string.ascii_lowercase)
    description = Faker('sentence', nb_words=8)
    anonymous_post = False
    visibility = Faker('random_element', elements=['public', 'private'])
    num_posts = 0
    community = SubFactory(CommunityFactory)

    @post_generation
    def members(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.members.add(*extracted)

class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    title = Faker('sentence', nb_words=5)
    body = Faker('paragraph', nb_sentences=3)
    num_comments = 0
    author = SubFactory(UserFactory)
    subrabble = SubFactory(SubRabbleFactory)

    @post_generation
    def likes(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.likes.add(*extracted)

class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    id = Sequence(lambda n: f'cmt{n}')
    body = Faker('paragraph', nb_sentences=2)
    likes = 0
    base = SubFactory(PostFactory)
    author = SubFactory(UserFactory)
