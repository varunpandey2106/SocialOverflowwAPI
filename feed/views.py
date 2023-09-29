from django.shortcuts import render

# Create your views here.

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import FeedPost, FeedPostVote
from .serializers import FeedPostSerializer


## POST REQUESTS

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_feedpost(request):
    user = request.user
    data = request.data

    is_comment = data.get('isComment')
    if is_comment:
        parent = FeedPost.objects.get(id=data['postId'])
        feedpost = FeedPost.objects.create(
            parent=parent,
            user=user,
            content=data['content'],
        )
    else:
        feedpost = FeedPost.objects.create(
            user=user,
            content=data['content']
        )

    serializer = FeedPostSerializer(feedpost, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def reshare(request):
    user = request.user
    data = request.data
    original_feedpost = FeedPost.objects.get(id=data['id'])
    
    if original_feedpost.user == user:
        return Response({'detail': 'You cannot reshare your own feed post.'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        feedpost = FeedPost.objects.filter(
            reshare=original_feedpost,
            user=user,
        )
        if feedpost.exists():
            return Response({'detail': 'Already Reshared'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            feedpost = FeedPost.objects.create(
                reshare=original_feedpost,
                user=user,
            )
        
        serializer = FeedPostSerializer(feedpost, many=False)
        return Response(serializer.data)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_403_FORBIDDEN)
