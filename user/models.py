from django.db import models
from django.contrib.auth.models import User
import uuid 
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache 
from datetime import datetime, timezone, timedelta
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django_countries.fields import CountryField
from randompinfield import RandomPinField
import logging
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from rest_framework.exceptions import NotAcceptable
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings 
# Create your models here.

class TimeStampedModel(models.Model):
    created_at= models.DateTimeField(auto_now_add=True) #profile create time
    updated_at= models.DateTimeField(auto_now_add=True) #profile update time

    class Meta:
        abstract= True

def user_directory_path(instance, filename):
    return "users/{0}/{1}".format(instance.user.username,filename)

AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
                  'twitter': 'twitter', 'email': 'email', 'github':'github'}

class Profile(TimeStampedModel):
    GENDER_MALE='m'
    GENDER_FEMALE='f'

    GENDER_CHOICES=(
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female')
    )

    user= models.OneToOneField(User,related_name='profile', on_delete=models.CASCADE )
    profile_picture= models.ImageField(upload_to= user_directory_path, blank=True)
    phone_number= PhoneNumberField(blank= False)
    gender=models.CharField(max_length=1, choices=GENDER_CHOICES, blank=False)
    birth_date=models.DateField( null= True)
    about= models.TextField(blank=True)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))


    def __str__(self):
        return "% " % self.user.username
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
    
    @property
    def last_seen(self):
        return cache.get(f"seen_{self.user.username}")
    
    @property #calculates online/offline status timestamp of last activity
    def online(self):
        if self.last_seen:
            now= datetime.now(timezone.utc)
            if now> self.last_seen+ timedelta(minutes=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False
        

@receiver(post_save,sender=User)
def create_user_profile(sender, instance,created,*args, **kwargs):
    if created:
        Profile.objects.create(user=instance)