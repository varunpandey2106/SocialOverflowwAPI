from rest_framework import serializers
from .models import Thread, UserMessage
from user.serializers import UserProfileSerializer

class MessageSerializer(serializers.ModelSerializer):
    sender = UserProfileSerializer(read_only=True)
    class Meta:
        model = UserMessage
        fields = '__all__'


