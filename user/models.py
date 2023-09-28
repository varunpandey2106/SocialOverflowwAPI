from django.db import models
from django.contrib.auth.models import User
import uuid 

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

