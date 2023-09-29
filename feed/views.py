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
    
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def update_vote(request):
    user = request.user 
    data = request.data

    feedpost = FeedPost.objects.get(id=data['post_id'])
    
    # What if the user is trying to remove their vote?
    vote, created = FeedPostVote.objects.get_or_create(feedpost=feedpost, user=user)

    if vote.value == data.get('value'):
        # If the same value is sent, the user is clicking on the vote to remove it
        vote.delete()
    else:
        vote.value = data['value']
        vote.save()

    # We re-query the feedpost to get the latest vote rank value
    feedpost = FeedPost.objects.get(id=data['post_id'])
    serializer = FeedPostSerializer(feedpost, many=False)

    return Response(serializer.data)

## GET REQUESTS

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def feed_posts(request):
    query = request.query_params.get('q')
    if query is None:
        query = ''

    user = request.user
    following = user.following.select_related('user')
    following_ids = [following_user.user.id for following_user in following]
    following_ids.append(user.id)

    # Query 5 feed posts from users you follow | TOP PRIORITY
    feed_posts = FeedPost.objects.filter(
        parent=None, user__id__in=following_ids
    ).order_by("-created")[:5]

    # Query recent feed posts with positive vote rank and no reshare
    recent_feed_posts = FeedPost.objects.filter(
        Q(parent=None) & Q(vote_rank__gte=0) & Q(reshare=None)
    ).order_by("-created")[:5]

    # Query top-ranked feed posts and append them to the original queryset
    top_feed_posts = FeedPost.objects.filter(Q(parent=None)).order_by("-vote_rank", "-created")

    # Add top-ranked feed posts to the feed after prioritizing the follow list
    for feed_post in recent_feed_posts:
        if feed_post not in feed_posts:
            feed_posts.insert(0, feed_post)

    for feed_post in top_feed_posts:
        if feed_post not in feed_posts:
            feed_posts.append(feed_post)

    paginator = PageNumberPagination()
    paginator.page_size = 10
    result_page = paginator.paginate_queryset(feed_posts, request)
    serializer = FeedPostSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def feedpost_details(request, pk):
    try:
        feedpost = FeedPost.objects.get(id=pk)  
        serializer = FeedPostSerializer(feedpost, many=False)
        return Response(serializer.data)
    except FeedPost.DoesNotExist:
        message = {
            'detail': 'Feed Post doesn\'t exist'
        }
        return Response(message, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def feedpost_comments(request, pk):
    try:
        feedpost = FeedPost.objects.get(id=pk)  
        comments = feedpost.feedpost_set.all()  
        serializer = FeedPostSerializer(comments, many=True)
        return Response(serializer.data)
    except FeedPost.DoesNotExist: 
        message = {
            'detail': 'Feed Post doesn\'t exist'
        }
        return Response(message, status=status.HTTP_404_NOT_FOUND)
    

## PATCH REQUESTS

@api_view(['PATCH'])
@permission_classes((IsAuthenticated,))
def edit_feedpost(request, pk):
    user = request.user
    data = request.data

    try:
        feedpost = FeedPost.objects.get(id=pk) 
        if user != feedpost.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            serializer = FeedPostSerializer(feedpost, data=data)  # Use FeedPostSerializer
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    except FeedPost.DoesNotExist: 
        return Response(status=status.HTTP_204_NO_CONTENT)


## DELETE

@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def delete_feedpost(request, pk):
    user = request.user
    try:
        feedpost = FeedPost.objects.get(id=pk)  
        if user != feedpost.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            feedpost.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    except FeedPost.DoesNotExist: 
        return Response({'details': 'Feed Post doesn\'t exist'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'details': str(e)}, status=status.HTTP_204_NO_CONTENT)


