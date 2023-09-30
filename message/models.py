from django.db import models
from user.models import UserProfile
import uuid

# Create your models here.

class Thread(models.Model): #thread of messages between 2 users
    id = models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)
    sender = models.ForeignKey(UserProfile,on_delete=models.SET_NULL,null=True,related_name="sender")
    reciever = models.ForeignKey(UserProfile,on_delete=models.SET_NULL,null=True,related_name="reciever")
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.sender.username + " and " + self.reciever.username)
    
class UserMessage(models.Model): #individual message in a thread
    id = models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)
    thread = models.ForeignKey(
        Thread, on_delete=models.CASCADE,related_name="messages")
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    body = models.TextField(null=True,blank=True)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.body)
