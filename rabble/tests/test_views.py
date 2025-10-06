import pytest
from django.urls import reverse
from rabble.models import SubRabble, Post
from rabble.tests.factories import (
    CommunityFactory,
    SubRabbleFactory,
    PostFactory,
    CommentFactory,
    UserFactory,
)

@pytest.mark.django_db
def test_index_view(client):
    ##logging in a user to pass the protection
    user_password = 'password123'
    user = UserFactory.create(password=user_password)
    client.login(username=user.username, password=user_password)  

    community = CommunityFactory.create()
    subrabbles = SubRabbleFactory.create_batch(5, community=community)
    response = client.get(reverse('index'))
    assert response.status_code == 200
    html = response.content.decode()
    for subrabble in subrabbles:
        assert subrabble.name in html
        assert subrabble.description in html

@pytest.mark.django_db
def test_subrabble_detail_view(client):
    ##logging in a user
    user_password = 'password123'
    user = UserFactory.create(password=user_password)
    client.login(username=user.username, password=user_password)
    
    community = CommunityFactory.create()
    subrabble = SubRabbleFactory.create(community=community)
    posts = []
    for _ in range(5):
        post = PostFactory.create(subrabble=subrabble)
        CommentFactory.create(base=post)
        posts.append(post)
    response = client.get(reverse('subrabble-detail', args=[subrabble.id]))
    assert response.status_code == 200
    html = response.content.decode()
    for post in posts:
        assert post.title in html
        assert str(post.num_comments) in html

@pytest.mark.django_db
def test_post_create_view(client):
    user_password = 'password123'
    user = UserFactory.create(password=user_password)
    client.login(username=user.username, password=user_password)
    community = CommunityFactory.create()
    subrabble = SubRabbleFactory.create(community=community)
    post_data = {
        'title': 'Test Post Title',
        'body': 'This is a test post body.',
        'subrabble': subrabble.id,
        'author': user.id,
    }
    response = client.post(reverse('post-create', args=[subrabble.id]), post_data)
    assert response.status_code == 302
    post = Post.objects.latest('id')
    assert post.title == post_data['title']
    assert post.body == post_data['body']
    assert post.subrabble == subrabble
    assert post.author == user
