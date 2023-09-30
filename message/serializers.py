from rest_framework import serializers
from .models import Thread, UserMessage
from user.serializers import UserProfileSerializer

class MessageSerializer(serializers.ModelSerializer):
    sender = UserProfileSerializer(read_only=True)
    class Meta:
        model = UserMessage
        fields = '__all__'


#chat_messages, last_message, and un_read_count
# are custom fields that are not directly tied to fields in the Thread model.
# These fields will provide additional information about the thread when the serializer is used.

class ThreadSerializer(serializers.ModelSerializer):
    chat_messages = serializers.SerializerMethodField(read_only=True)
    last_message = serializers.SerializerMethodField(read_only=True)
    un_read_count = serializers.SerializerMethodField(read_only=True)
    sender = UserProfileSerializer(read_only=True)
    reciever = UserProfileSerializer(read_only=True)
    class Meta:
        model = Thread
        fields = ['id','updated','timestamp','sender','reciever','chat_messages','last_message','un_read_count']
#get_chat_messages is a custom method that retrieves and serializes the messages associated with the thread.
    def get_chat_messages(self,obj):
        messages = MessageSerializer(obj.messages.order_by('timestamp'),many=True)
        return messages.data
#get_last_message is a method that retrieves and serializes the last message in the thread based on the timestamp
    def get_last_message(self,obj):
        serializer = MessageSerializer(obj.messages.order_by('timestamp').last(),many=False)
        return serializer.data
#get_un_read_count calculates and returns the count of unread messages within the thread
    def get_un_read_count(self,obj):
        messages = obj.messages.filter(is_read=False).count()
        return messages
