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


# A topic tag is added to by the user so they can content on their feed with the 
# related tags that
# They have selected
class TopicTag(models.Model):
    name = models.CharField(primary_key=True, max_length=150, null=False, blank=False)

    def __str__(self):
        return self.name
    
# Skills are added by teh user to indicate topics they are proficient in
class SkillTag(models.Model):
    name = models.CharField(primary_key=True, max_length=150, null=False, blank=False)

    def __str__(self):
        return self.name
    
class Profile(TimeStampedModel):
    GENDER_MALE='m'
    GENDER_FEMALE='f'

    GENDER_CHOICES=(
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female')
    )

    user= models.OneToOneField(User,related_name='profile', on_delete=models.CASCADE )
    name = models.CharField(max_length=200, null=True)
    username = models.CharField(max_length=200, null=True)
    profile_picture= models.ImageField(upload_to= user_directory_path, blank=True)
    phone_number= PhoneNumberField(blank= False)
    gender=models.CharField(max_length=1, choices=GENDER_CHOICES, blank=False)
    birth_date=models.DateField( null= True)
    about= models.TextField(blank=True)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))
    vote_ratio = models.IntegerField(blank=True, null=True, default=0)
    followers_count = models.IntegerField(blank=True, null=True, default=0)
    skills = models.ManyToManyField(SkillTag, related_name='personal_skills', blank=True)
    interests = models.ManyToManyField(TopicTag, related_name='topic_interests', blank=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    email_verified = models.BooleanField(default=False)
    id = models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)


    def __str__(self):
        return str(self.user.username)
    
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

class SMSVerification(TimeStampedModel):
    user= models.OneToOneField(User, related_name= 'phone', on_delete=models.CASCADE)
    number= PhoneNumberField(unique= True)
    pin= RandomPinField(length=6)
    is_verified=models.BooleanField(default=False)
    sent= models.BooleanField(default=False)
    phone= PhoneNumberField(null= True)

    def send_confirmation(self):

        logging.debug("Sending PIN %s to phone %s" % (self.pin,self.phone))

        if all(
            [
                settings.TWILIO_ACCOUNT_SID,
                settings.TWILIO_AUTH_TOKEN,
                settings.TWILIO_FROM_NUMBER
            ]
        ):
            
            try:
                twilio_client=Client(
                    settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN
                )
                twilio_client.messages.create(
                    body="Your forgotten activation code is %s" % self.pin, 
                    to=str(self.user.profile.phone_number),
                    from_=settings.TWILIO_FROM_NUMBER,
                )

                self.sent=True
                self.save()
                return True
            except TwilioRestException as e:
                logging.error(e)
        else:
            logging.warning('Twilio credentials are not set')
    
    def confirm(self,pin):
        if pin==self.pin and self.verified==False:
            self.verified=True
            self.save()
        else:
            raise NotAcceptable("your pin is wrong, or this phone number has been verified before")
        
        return self.verified

@receiver(post_save,sender=Profile)
def send_sms_verification(sender, instance, *args, **kwargs):
    try:
        sms=instance.user.sms
        if sms:
            pin=sms.pin
            sms.delete()
            verification=SMSVerification.objects.create(
                user=instance.user,
                phone=instance.user.profile.phone_number,
                sent= True,
                verified=True,
                pin=pin,
            )

    
    except:
        if instance.user.profile.phone_number:
            verification=SMSVerification.objects.create(
                user=instance.user,phone=instance.user.profile.phone_number
            )
            # todo remove send_confirm and make view for it
            verification.send_confirmation()

class DeactivateUser(TimeStampedModel):
    user=models.OneToOneField(User, related_name='deactivate',on_delete=models.CASCADE)
    deactive=models.BooleanField(default=True)
