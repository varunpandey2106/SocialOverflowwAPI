from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from user.models import UserProfile
from .serializers import MessageSerializer , ThreadSerializer
from .models import UserMessage , Thread
from django.db.models import Q

# Create your views here.

##POST REQUESTS

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def CreateThread(request):
    sender = request.user.userprofile
    recipient_id = request.data.get('recipient_id')
    recipient = UserProfile.objects.get(id=recipient_id)
    if recipient_id is not None:
        try:
            thread,created = Thread.objects.get_or_create(sender=sender,reciever=recipient)
            serializer = ThreadSerializer(thread, many=False)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({'detail':'User with that id doesnt not exists'})
    else:
        return Response({'details':'Recipient id not found'})
    
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_message(request):
    sender = request.user.userprofile
    data = request.data
    thread_id = data.get('thread_id')
    if thread_id:
        message = data.get('message')
        thread= Thread.objects.get(id=thread_id)
        if thread:
            if message is not None:
                message = UserMessage.objects.create(thread=thread,sender=sender,body=message)
                message.save()
                serializer = ThreadSerializer(thread, many=False)
                return Response(serializer.data)
            else:
                return Response({'details':'Content for message required'})
        else:
            return Response({'details':'Thread not found'})
    else:
        return Response({'details':'Please provide other user id'})


##GET REQUESTS

