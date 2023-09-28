from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile, TopicTag, SkillTag

#tags
class TopicTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicTag
        fields = '__all__'

class SkillTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillTag
        fields = '__all__'

#user
class UserProfileSerializer(serializers.ModelSerializer):
    profile_pic = serializers.SerializerMethodField(read_only=True)
    interests = TopicTagSerializer(many=True, read_only=True)
    skills = SkillTagSerializer(many=True, read_only=True)
    class Meta:
        model = UserProfile
        fields = '__all__'

    def get_profile_pic(self, obj):
        try:
            pic = obj.profile_pic.url
        except:
            pic = None
        return pic

class CurrentUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'profile', 'username', 'email', 'is_superuser', 'is_staff']

    def get_profile(self, obj):
        profile = obj.userprofile if hasattr(obj, 'userprofile') else None
        serializer = UserProfileSerializer(profile, many=False)
        return serializer.data  # Corrected method to return serialized profile

    
class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'profile', 'username', 'is_superuser', 'is_staff']

    def get_profile(self, obj):
        profile = obj.userprofile if hasattr(obj, 'userprofile') else None
        serializer = UserProfileSerializer(profile, many=False)
        return serializer.data  # Corrected method to return serialized profile

class UserSerializerWithToken(UserSerializer):
    access = serializers.SerializerMethodField(read_only=True)
    refresh = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        exclude = ['password']

    def get_access(self, obj):
        token = RefreshToken.for_user(obj)

        # Use obj.userprofile if necessary; make sure the field exists
        user_profile = obj.userprofile if hasattr(obj, 'userprofile') else None

        token_data = {
            'username': obj.username,
            'name': user_profile.name if user_profile else None,
            'profile_pic': user_profile.profile_pic.url if user_profile else None,
            'is_staff': obj.is_staff,
            'id': obj.id,
        }

        token.update(token_data)
        return str(token.access_token)

    def get_refresh(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token)



