import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rabble.models import Post
from rabble.tests.factories import (
    CommunityFactory,
    SubRabbleFactory,
    PostFactory,
    CommentFactory,
    UserFactory,
)

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_subrabble_get(api_client):
    community = CommunityFactory.create()
    subrabble = SubRabbleFactory.create(community=community)
    response = api_client.get(reverse('api-subrabble-detail', args=[subrabble.id]))
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['id'] == subrabble.id
    assert data['name'] == subrabble.name
    assert data['description'] == subrabble.description

@pytest.mark.django_db
def test_post_post(api_client):
    user = UserFactory.create()
    community = CommunityFactory.create()
    subrabble = SubRabbleFactory.create(community=community)
    api_client.force_authenticate(user=user)

    post_data = {
        'title': 'Test API Post',
        'body': 'This is a post created via the API.',
        'author': user.username,
        'subrabble': subrabble.id
    }

    response = api_client.post(
        reverse('api-post-list-create', args=[subrabble.id]),
        post_data
    )

    print(response.status_code)
    print(response.data)

    assert response.status_code == status.HTTP_201_CREATED

    post = Post.objects.get(pk=response.data['id'])
    assert post.title == post_data['title']
    assert post.body == post_data['body']
    assert post.author == user
    assert post.subrabble == subrabble

@pytest.mark.django_db
def test_post_patch(api_client):
    user = UserFactory.create()
    community = CommunityFactory.create()
    subrabble = SubRabbleFactory.create(community=community)
    post = PostFactory.create(subrabble=subrabble, author=user)
    api_client.force_authenticate(user=user)
    patch_data = {'title': 'Updated Post Title'}
    response = api_client.patch(
        reverse('api-post-detail', args=[subrabble.id, post.pk]),
        patch_data
    )
    assert response.status_code == status.HTTP_200_OK
    post.refresh_from_db()
    assert post.title == patch_data['title']
