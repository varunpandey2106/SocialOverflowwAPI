from rest_framework import serializers
from django.contrib.auth.models import User

from .models import FeedPost
from user.serializers import UserProfileSerializer, UserSerializer

class FeedPostSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    original_feedpost = serializers.SerializerMethodField(read_only=True)
    up_voters = serializers.SerializerMethodField(read_only=True)
    down_voters = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FeedPost  # Use the FeedPost model
        fields = '__all__'

    def get_user(self, obj):
        user = obj.user.userprofile
        serializer = UserProfileSerializer(user, many=False)
        return serializer.data

    def get_original_feedpost(self, obj):
        original = obj.reshare  # Use 'reshare' instead of 'remumble'
        if original:
            serializer = FeedPostSerializer(original, many=False)
            return serializer.data
        else:
            return None

    def get_up_voters(self, obj):
        # Returns list of users that upvoted post
        voters = obj.votes.through.objects.filter(feedpost=obj, value='upvote').values_list('user', flat=True)
        voter_objects = obj.votes.filter(id__in=voters)
        serializer = UserSerializer(voter_objects, many=True)
        return serializer.data

    def get_down_voters(self, obj):
        # Returns list of users that downvoted post (changed from upvoted)
        voters = obj.votes.through.objects.filter(feedpost=obj, value='downvote').values_list('user', flat=True)
        voter_objects = obj.votes.filter(id__in=voters)
        serializer = UserSerializer(voter_objects, many=True)
        return serializer.data
