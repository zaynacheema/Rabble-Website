from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    photo = models.ImageField(upload_to='user_photos/', blank=True, null=True)
    bio = models.TextField(blank=True)
    interests = models.TextField(blank=True)
#already inheriting from abstract user so not including user, first name, last name, email


class CommunityMembership(models.Model):
    class Role(models.TextChoices):
        OWNER = 'Owner'
        ADMIN = 'Admin'
        MEMBER = 'Member'

    community = models.ForeignKey('Community', on_delete= models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices= Role.choices)

    class Meta:
        unique_together = ['community', 'user']

class Community(models.Model):
    members = models.ManyToManyField('User', through='CommunityMembership')
#has id by default

class Conversation(models.Model):
    title = models.TextField()
    messages = models.TextField(blank=True)
#has id by default

class ConversationMembership(models.Model):
    conversation = models.ForeignKey('Conversation', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['conversation', 'user']


class SubRabble(models.Model):
    id = models.CharField(primary_key=True, max_length= 100)
    name = models.CharField(max_length=255)
    description = models.TextField()
    anonymous_post = models.BooleanField(default= False)
    visibility = models.CharField(max_length=50)
    num_posts = models.PositiveIntegerField(default=0)
    members = models.ManyToManyField('User')
    community = models.ForeignKey('Community', on_delete=models.CASCADE)

class Post(models.Model):
#id = models.CharField(primary_key=True, max_length=100)
#encountering error so im going to let django use default
    title = models.TextField()
    body = models.TextField()
    likes = models.ManyToManyField('User', related_name='liked_posts', blank=True)  
    num_comments = models.PositiveIntegerField(default=0)

    author = models.ForeignKey('User', on_delete=models.CASCADE)
    subrabble = models.ForeignKey('SubRabble', on_delete=models.CASCADE)

class Comment(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    body = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    base = models.ForeignKey('Post', on_delete=models.CASCADE)
    author = models.ForeignKey('User', on_delete=models.CASCADE)

