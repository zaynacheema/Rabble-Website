from django.urls import path
from . import views

urlpatterns = [
  path('subrabbles', views.subrabble_list, name='api-subrabble-list'),
  path('subrabbles/!<str:identifier>', views.subrabble_detail, name='api-subrabble-detail'),
  path('subrabbles/!<str:identifier>/posts', views.PostListCreate.as_view(), name='api-post-list-create'),
  path('subrabbles/!<str:identifier>/posts/<int:pk>', views.PostRetrieveUpdateDelete.as_view(), name='api-post-detail'),
  path('subrabbles/!<str:identifier>/posts/<int:pk>/likes', views.toggle_like, name='api-post-toggle-like')
]

