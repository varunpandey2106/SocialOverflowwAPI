from django.contrib import admin
from .models import FeedPost, FeedPostVote

# Register your models here.
admin.site.register(FeedPost)
admin.site.register(FeedPostVote)
