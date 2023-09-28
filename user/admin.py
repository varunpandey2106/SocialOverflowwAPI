from django.contrib import admin
from .models import UserProfile, TopicTag, SkillTag, SMSVerification, DeactivateUser

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(TopicTag)
admin.site.register(SkillTag)
admin.site.register(SMSVerification)
admin.site.register(DeactivateUser)