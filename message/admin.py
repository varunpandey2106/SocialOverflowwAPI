from django.contrib import admin
from .models import Thread, UserMessage

# Register your models here.

admin.site.register(Thread)
admin.site.register(UserMessage)
