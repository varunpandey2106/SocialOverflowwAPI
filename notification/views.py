from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from user.models import UserProfile
from .models import Notification
from .serializers import NotificationSerializer

# Create your views here.

##GET REQUEST

#This view retrieves a list of notifications for the authenticated user.
#It accepts an optional query parameter, is_read, which filters notifications based on their read status (read or unread).

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_notifications(request):
    is_read = request.query_params.get('is_read')
    if is_read == None:
        notifications = request.user.notifications.order_by('-created')
    else:
        notifications = request.user.notifications.filter(is_read=is_read).order_by('-created')
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)

##PUT REQUEST

#This view marks a specific notification as read and deletes it.
#It accepts the pk (primary key) of the notification to be marked as read.
@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def read_notification(request, pk):
    try:
        notification = Notification.objects.get(id=pk)
        if notification.to_user == request.user:
            notification.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'details': f"{e}"},status=status.HTTP_204_NO_CONTENT)
