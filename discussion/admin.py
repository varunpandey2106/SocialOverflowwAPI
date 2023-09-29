from django.contrib import admin
from .models import Discussion, DiscussionComment, DiscussionVote

# Register your models here.

admin.site.register(Discussion)
admin.site.register(DiscussionComment)
admin.site.register(DiscussionVote)
