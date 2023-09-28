from django.shortcuts import render
import datetime
import uuid
import random
import os.path

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
#email verification imports
from django.contrib.auth.tokens import default_token_generator
from django.core.files.storage import default_storage
# from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models import Q , Count
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from email_validator import validate_email, EmailNotValidError
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# from article.serializers import ArticleSerializer
# from feed.serializers import MumbleSerializer
# from notification.models import Notification

from .models import UserProfile, SkillTag, TopicTag
from .serializers import (UserProfileSerializer, UserSerializer,
                          UserSerializerWithToken, CurrentUserSerializer)

# Create your views here.


def email_validator(email):
    """validates & return the entered email if correct
    else returns an exception as string"""
    try:
        validated_email_data = validate_email(email)
        email_add = validated_email_data['email']
        return email_add
    except EmailNotValidError as e:
        return str(e)