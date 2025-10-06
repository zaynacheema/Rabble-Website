from django.contrib import admin

# Register your models here.

# :)

from .models import User, Post, Comment, SubRabble, Community, CommunityMembership, Conversation, ConversationMembership

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(SubRabble)
admin.site.register(Community)
admin.site.register(CommunityMembership)
admin.site.register(Conversation)
admin.site.register(ConversationMembership)

