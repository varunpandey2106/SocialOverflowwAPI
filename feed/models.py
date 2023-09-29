from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import uuid


# Create your models here.

class FeedPost(models.Model):
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    # For reshare functionality
    reshare = models.ForeignKey("self", on_delete=models.CASCADE, related_name='reshares', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = RichTextField(null=True, blank=True)
    image = models.ImageField(blank=True, null=True)
    vote_rank = models.IntegerField(blank=True, null=True, default=0)
    comment_count = models.IntegerField(blank=True, null=True, default=0)
    share_count = models.IntegerField(blank=True, null=True, default=0)
    created = models.DateTimeField(auto_now_add=True)
    votes = models.ManyToManyField(User, related_name='feedpost_votes', blank=True, through='FeedPostVote')
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        try:
            content = self.content[:80]
        except Exception:
            content = 'Reshared: ' + str(self.reshare.content[:80])
        return content

    @property
    def shares(self):
        queryset = self.reshares.all()
        return queryset

    @property
    def comments(self):
        queryset = FeedPost.objects.filter(parent=self)
        return queryset


    
